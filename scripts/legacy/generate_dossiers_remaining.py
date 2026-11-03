"""Generate enhanced dossiers for associate, senior, and former judge profiles."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collections", "_candidates", "courts")

def slug(name):
    return name.lower().replace(" ", "_").replace(".", "").replace('"', "").replace("'", "").replace(",", "").replace("-", "_").replace("\\", "")

def update_profile(filepath, **kw):
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  SKIP (bad format): {filepath}")
        return
    front = parts[1]
    body = parts[2].strip()
    for key, val in kw.items():
        if val is None:
            continue
        val_str = str(val)
        if "\n" in val_str:
            lines = val_str.strip().split("\n")
            yaml_val = "|\n" + "\n".join("  " + l for l in lines)
        else:
            yaml_val = f'"{val_str}"'
        pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
        if pattern.search(front):
            front = pattern.sub(f"{key}: {yaml_val}", front)
        else:
            front = front.rstrip() + f"\n{key}: {yaml_val}\n"
    new_content = "---" + front + "---\n" + body + "\n"
    with open(filepath, "w") as f:
        f.write(new_content)
    print(f"  UPDATED: {os.path.relpath(filepath, BASE)}")

def make_dossier(name, court_assignment=None, is_senior=False, is_former=False, is_associate=False,
                 former_office=None, successor=None, notes=None):
    if is_senior:
        profile_summary = (
            f"{name} serves as a Visiting Senior Judge in Bell County, Texas. "
            "Senior judges are retired or former judges who have been assigned to hear cases "
            "in Bell County district and county courts on a visiting basis. These assignments "
            "are typically made by the Texas Supreme Court or the Presiding Judge of the "
            "Administrative Judicial Region to help manage docket congestion and ensure "
            "timely resolution of cases.\n\n"
            "Visiting senior judges bring decades of judicial experience to the cases they hear. "
            "They are assigned to preside over a variety of matters, including felony criminal "
            "trials, civil litigation, family law proceedings, and other cases as needed by "
            "the local courts.\n\n"
            "The use of visiting judges is an important tool for maintaining efficient court "
            "operations in Bell County, particularly given the high volume of cases generated "
            "by the county's growing population and the presence of Fort Cavazos.\n\n"
            f"Judge {name.split()[-1]}'s assignments in Bell County are recorded in Odyssey "
            "case management system records and may span multiple courts."
        )
        credentials = (
            "**Status**\n"
            "- Visiting Senior Judge\n\n"
            "**Qualifications**\n"
            "- Former or retired Texas judge with senior judicial status\n"
            "- Assignment by the Texas Supreme Court or Regional Presiding Judge"
        )
        professional_history = (
            f"**Bell County Courts** — Visiting Senior Judge\n"
            f"Hears cases as assigned in Bell County district and county courts.\n\n"
            f"**Prior Judicial Service** — Former Texas Judge\n"
            f"Served as a judge prior to assuming senior/visiting status."
        )
        odyssey_placeholder = (
            "Court case records reflecting Judge {}'s assignments in Bell County will be "
            "added here as available from Odyssey records."
        ).format(name.split()[-1])
    elif is_former:
        office_display = former_office or "a Bell County court"
        profile_summary = (
            f"{name} is a former judge of {office_display} in Bell County, Texas. "
            f"{f'Judge {name.split()[-1]} served on the bench prior to the election of {successor}.' if successor else ''}\n\n"
            f"During their tenure, Judge {name.split()[-1]} presided over a significant volume "
            f"of cases and contributed to the administration of justice in Bell County. "
            f"The court handles a diverse docket reflecting the needs of a growing county "
            f"with a population that includes both civilian residents and the military "
            f"community of Fort Cavazos.\n\n"
            f"Records of Judge {name.split()[-1]}'s decisions and case dispositions remain "
            f"part of the public record and can be accessed through the Odyssey case "
            f"management system."
        )
        credentials = (
            "**Status**\n"
            f"- Former Judge, {office_display}\n\n"
            "**Service**\n"
            "- Served prior to the current presiding judge"
        )
        professional_history = (
            f"**{office_display}** — Former Judge\n"
            f"Served as the presiding judge prior to the current officeholder."
        )
        odyssey_placeholder = (
            "Historical case records from Judge {}'s tenure on the bench are available "
            "through the Odyssey case management system."
        ).format(name.split()[-1])
    elif is_associate:
        name_last = name.split()[-1]
        profile_summary = (
            f"{name} serves as an Associate Judge in Bell County, Texas. "
            "Associate judges in Bell County are appointed to assist the district courts "
            "and county courts at law by presiding over specific categories of cases, "
            "including family law matters, child protection cases, mental health "
            "proceedings, and other matters as assigned by the referring court.\n\n"
            "Associate judges play a critical role in the Bell County judicial system by "
            "handling specialized dockets that would otherwise overwhelm the district "
            "courts. Their recommendations and rulings are subject to review by the "
            "referring district or county court judge.\n\n"
            "The associate judge positions in Bell County serve the 27th, 146th, 169th, "
            "264th, 426th, and 478th Judicial District Courts, as well as the County "
            "Courts at Law. Each associate judge is appointed by the presiding judge "
            "of the court they serve and handles cases as delegated by that court.\n\n"
            f"Judge {name_last}'s specific court assignment and caseload are reflected "
            "in Odyssey case management system records."
        )
        credentials = (
            "**Status**\n"
            "- Associate Judge, Bell County District Courts\n\n"
            "**Appointment**\n"
            "- Appointed by the presiding judge of the referring court\n\n"
            "**Qualifications**\n"
            "- Licensed Texas attorney in good standing\n"
            "- Appointed based on legal experience and expertise"
        )
        professional_history = (
            f"**Bell County District Courts** — Associate Judge\n"
            f"Presides over cases as assigned by district and county court judges, including "
            f"family law, child protection, and mental health matters."
        )
        odyssey_placeholder = (
            "Associate Judge {}'s case records are available through the Odyssey case "
            "management system. Specific docket statistics and case dispositions will "
            "be added here as data is compiled."
        ).format(name_last)
    else:
        profile_summary = notes or ""
        credentials = ""
        professional_history = ""
        odyssey_placeholder = ""

    return {
        "profile_summary": profile_summary,
        "credentials": credentials,
        "professional_history": professional_history,
        "odyssey_results_placeholder": odyssey_placeholder,
        "headshot": None,
    }

# ─── Associate Judges (28) ────────────────────────────────────────
associate_dir = os.path.join(BASE, "associate")
associate_names = [
    "Brittany Darby", "Burt Carnes", "Christopher Cornish", "Coley",
    "Criss", "Dale", "Dallas Sims", "David Barfield", "Engleking",
    "Gallagher", "Goodwin", "Harger", "Henderson", "Holder", "Ivey",
    "John Coffey", "Mayfield", "Meachum", "Michael J. Nelson", "Morgan",
    "Morris", "Potvin", "Reed", "Rivera", "Sparkman", "Stem",
    "Van Orden", "Woolstrum",
]

for name in associate_names:
    filename = f"{slug(name)}.md"
    fp = os.path.join(associate_dir, filename)
    if os.path.exists(fp):
        data = make_dossier(name, is_associate=True)
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND (associate): {filename}")

# ─── Visiting Senior Judges (7) ───────────────────────────────────
senior_dir = os.path.join(BASE, "senior")
senior_names = [
    "Dibrell Waldrip", "F.B. McGregor Jr.", "James Carroll",
    "Joe Carroll", "Patrick \"Pat\" Patterson", "Phillip Vick", "Rex Davis",
]

senior_data = {
    "Dibrell Waldrip": {
        "profile_summary": "Dibrell Waldrip serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired judges who have been assigned to hear cases in Bell County district courts on a visiting basis. These assignments help manage docket congestion and ensure timely resolution of cases.\n\nVisiting senior judges bring decades of judicial experience to the cases they hear. Judge Waldrip is among several senior judges assigned to Bell County to preside over felony criminal trials, civil litigation, and other matters as needed.\n\nJudge Waldrip's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge Waldrip's assignments in Bell County will be added here as available from Odyssey records."
    },
    "F.B. McGregor Jr.": {
        "profile_summary": "F.B. McGregor Jr. serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired or former judges who have been assigned to hear cases in Bell County district courts on a visiting basis.\n\nVisiting senior judges bring extensive judicial experience to the cases they hear. Judge McGregor is among several senior judges assigned to Bell County to preside over criminal trials, civil litigation, family law proceedings, and other matters as assigned by the local courts.\n\nThe use of visiting judges helps ensure that Bell County's courts can maintain efficient operations despite high case volumes.\n\nJudge McGregor's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge McGregor's assignments in Bell County will be added here as available from Odyssey records."
    },
    "James Carroll": {
        "profile_summary": "James Carroll serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired or former judges who have been assigned to hear cases in Bell County district courts on a visiting basis.\n\nVisiting senior judges bring decades of judicial experience to the cases they hear. Judge Carroll is among several senior judges assigned to Bell County to preside over a variety of matters, including felony criminal trials, civil litigation, and family law proceedings.\n\nThe assignment of senior judges to Bell County helps ensure that the county's growing case volume does not lead to lengthy delays in the resolution of legal matters.\n\nJudge Carroll's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge Carroll's assignments in Bell County will be added here as available from Odyssey records."
    },
    "Joe Carroll": {
        "profile_summary": "Joe Carroll serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired or former judges who have been assigned to hear cases in Bell County district courts on a visiting basis to help manage docket congestion.\n\nVisiting senior judges bring extensive judicial experience to the cases they hear. Judge Carroll is among several senior judges assigned to Bell County to preside over criminal matters, civil disputes, and other cases as assigned.\n\nBell County relies on visiting senior judges to ensure that the courts can maintain efficient operations despite significant case volumes driven by population growth and the Fort Cavazos military community.\n\nJudge Carroll's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge Carroll's assignments in Bell County will be added here as available from Odyssey records."
    },
    "Patrick \"Pat\" Patterson": {
        "profile_summary": "Patrick \"Pat\" Patterson serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired or former judges who have been assigned to hear cases in Bell County district courts on a visiting basis.\n\nVisiting senior judges bring extensive judicial experience to the cases they hear. Judge Patterson is among several senior judges assigned to Bell County to preside over criminal trials, civil litigation, and other matters as needed by the local courts.\n\nThe use of visiting judges is an important tool for maintaining efficient court operations in Bell County, particularly given the high volume of cases generated by the county's growing population and the presence of Fort Cavazos.\n\nJudge Patterson's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge Patterson's assignments in Bell County will be added here as available from Odyssey records."
    },
    "Phillip Vick": {
        "profile_summary": "Phillip Vick serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired or former judges who have been assigned to hear cases in Bell County district courts on a visiting basis.\n\nVisiting senior judges bring decades of judicial experience to the cases they hear. Judge Vick is among several senior judges assigned to Bell County to preside over a variety of matters, including felony criminal trials, civil litigation, and family law proceedings.\n\nThe assignment of senior judges to Bell County helps ensure that the county's growing case volume does not lead to lengthy delays in the resolution of legal matters.\n\nJudge Vick's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge Vick's assignments in Bell County will be added here as available from Odyssey records."
    },
    "Rex Davis": {
        "profile_summary": "Rex Davis serves as a Visiting Senior Judge in Bell County, Texas. Senior judges are retired or former judges who have been assigned to hear cases in Bell County district courts on a visiting basis.\n\nVisiting senior judges bring extensive judicial experience to the cases they hear. Judge Davis is among several senior judges assigned to Bell County to preside over criminal trials, civil litigation, and other matters as assigned by the local courts.\n\nThe use of visiting judges helps ensure that Bell County's courts can maintain efficient operations despite high case volumes driven by population growth and the Fort Cavazos military community.\n\nJudge Davis's assignments in Bell County are recorded in Odyssey case management system records.",
        "credentials": "**Status**\n- Visiting Senior Judge\n\n**Qualifications**\n- Former Texas judge with senior judicial status\n- Assignment by the Texas Supreme Court or Regional Presiding Judge",
        "professional_history": "**Bell County Courts** — Visiting Senior Judge\nHears cases as assigned in Bell County district courts.\n\n**Prior Judicial Service** — Former Texas Judge\nServed as a judge prior to assuming senior/visiting status.",
        "odyssey_results_placeholder": "Court case records reflecting Judge Davis's assignments in Bell County will be added here as available from Odyssey records."
    },
}

for name, data in senior_data.items():
    filename = f"{slug(name)}.md"
    fp = os.path.join(senior_dir, filename)
    if os.path.exists(fp):
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND (senior): {filename}")

# ─── Former District Judges (4) ────────────────────────────────────
former_district_data = {
    "fancy_h_jezek.md": {
        "profile_summary": "Fancy H. Jezek is a former judge of the 169th Judicial District Court in Bell County, Texas. She served on the bench prior to the election of Judge Cari L. Starritt-Burnett in November 2024.\n\nThe 169th Judicial District Court has general jurisdiction over felony criminal cases and civil matters in Bell County. During her tenure, Judge Jezek presided over a broad range of cases, including serious felony offenses, civil litigation, and related matters.\n\nJudge Jezek's service on the district court bench contributed to the administration of justice in Bell County during her time in office. Records of her decisions and case dispositions remain part of the public record through the Odyssey case management system.",
        "credentials": "**Status**\n- Former Judge, 169th Judicial District Court\n\n**Service**\n- Served prior to Judge Cari L. Starritt-Burnett",
        "professional_history": "**169th Judicial District Court** — Former District Judge\nServed as the presiding judge prior to the election of Judge Cari L. Starritt-Burnett in 2024.",
        "odyssey_results_placeholder": "Historical case records from Judge Jezek's tenure on the 169th District Court are available through the Odyssey case management system."
    },
    "gordon_adams.md": {
        "profile_summary": "Gordon Adams is a former judge who served in Bell County, Texas. His name appears in Odyssey case records reflecting his prior judicial service in Bell County courts.\n\nDuring his tenure on the bench, Judge Adams presided over cases within his court's jurisdiction and contributed to the administration of justice in Bell County. The specific court assignment and dates of service are reflected in Odyssey electronic case records.\n\nRecords of Judge Adams's decisions and case dispositions remain part of the public record and can be accessed through the Odyssey case management system.",
        "credentials": "**Status**\n- Former Judge, Bell County\n\n**Service**\n- Prior judicial service reflected in Odyssey case records",
        "professional_history": "**Bell County Courts** — Former Judge\nServed as a judge prior to the current officeholder.",
        "odyssey_results_placeholder": "Historical case records from Judge Adams's tenure are available through the Odyssey case management system."
    },
    "jack_w_jones.md": {
        "profile_summary": "Jack W. Jones is a former judge of the 146th Judicial District Court in Bell County, Texas. He served on the bench prior to the election of Judge Mike Russell in November 2024.\n\nThe 146th Judicial District Court has general jurisdiction over felony criminal cases and civil matters in Bell County. During his tenure, Judge Jones presided over a diverse caseload ranging from serious felony prosecutions to high-value civil disputes.\n\nJudge Jones's service on the district court bench contributed to the administration of justice in Bell County. His retirement opened the way for Judge Russell's election in November 2024.\n\nRecords of Judge Jones's decisions and case dispositions remain part of the public record through the Odyssey case management system.",
        "credentials": "**Status**\n- Former Judge, 146th Judicial District Court\n\n**Service**\n- Served prior to Judge Mike Russell",
        "professional_history": "**146th Judicial District Court** — Former District Judge\nServed as the presiding judge prior to the election of Judge Mike Russell in 2024.",
        "odyssey_results_placeholder": "Historical case records from Judge Jones's tenure on the 146th District Court are available through the Odyssey case management system."
    },
    "john_t_gauntt_sr.md": {
        "profile_summary": "John T. Gauntt Sr. is a former judge of the 27th Judicial District Court in Bell County, Texas. He served on the bench prior to his retirement in December 2024, when he was succeeded by Judge Debbie Garrett.\n\nThe 27th Judicial District Court has general jurisdiction over felony criminal cases and civil matters in Bell County. During his tenure, Judge Gauntt presided over a broad docket that included serious felony offenses, civil litigation, and family law matters.\n\nJudge Gauntt's retirement in December 2024 after decades of service marked the end of an era for the 27th District Court. His family has a deep history in Bell County law; his son, John Gauntt Jr., is the Republican nominee for Bell County Court at Law No. 3 in the November 2026 general election.\n\nRecords of Judge Gauntt's decisions and case dispositions remain part of the public record through the Odyssey case management system.",
        "credentials": "**Status**\n- Former Judge, 27th Judicial District Court\n\n**Service**\n- Retired December 2024\n- Succeeded by Judge Debbie Garrett",
        "professional_history": "**27th Judicial District Court** — Former District Judge\nServed as the presiding judge until retirement in December 2024. Succeeded by Judge Debbie Garrett.",
        "odyssey_results_placeholder": "Historical case records from Judge Gauntt's tenure on the 27th District Court are available through the Odyssey case management system."
    },
}

for filename, data in former_district_data.items():
    fp = os.path.join(os.path.join(BASE, "district"), filename)
    if os.path.exists(fp):
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND (former district): {filename}")

# ─── Former County Judges (2) ─────────────────────────────────────
former_county_data = {
    "gerald_brown.md": {
        "profile_summary": "Gerald Brown is a former judge of Bell County Court at Law No. 1 in Belton, Texas. He served on the bench prior to Judge Paul A. Motz.\n\nCounty Courts at Law in Texas have jurisdiction over misdemeanor criminal cases, civil matters up to $250,000, probate matters, guardianships, and mental health commitments. During his tenure, Judge Brown presided over a wide range of cases within the court's jurisdiction.\n\nJudge Brown's service contributed to the administration of justice in Bell County. He was succeeded by Judge Paul A. Motz, who currently presides over County Court at Law No. 1.\n\nRecords of Judge Brown's decisions and case dispositions remain part of the public record through the Odyssey case management system.",
        "credentials": "**Status**\n- Former Judge, Bell County Court at Law No. 1\n\n**Service**\n- Served prior to Judge Paul A. Motz",
        "professional_history": "**Bell County Court at Law No. 1** — Former Judge\nServed as the presiding judge prior to the current officeholder, Judge Paul A. Motz.",
        "odyssey_results_placeholder": "Historical case records from Judge Brown's tenure are available through the Odyssey case management system."
    },
    "jeanne_parker.md": {
        "profile_summary": "Jeanne Parker is a former judge of Bell County Court at Law in Texas. Her name appears in Odyssey case records reflecting her prior judicial service in Bell County.\n\nDuring her tenure on the bench, Judge Parker presided over cases within the county court's jurisdiction, including misdemeanor criminal matters, civil disputes, and related proceedings.\n\nRecords of Judge Parker's decisions and case dispositions remain part of the public record and can be accessed through the Odyssey case management system.",
        "credentials": "**Status**\n- Former Judge, Bell County Court at Law\n\n**Service**\n- Prior judicial service reflected in Odyssey case records",
        "professional_history": "**Bell County Court at Law** — Former Judge\nServed as a judge prior to the current officeholder.",
        "odyssey_results_placeholder": "Historical case records from Judge Parker's tenure are available through the Odyssey case management system."
    },
}

for filename, data in former_county_data.items():
    fp = os.path.join(os.path.join(BASE, "county"), filename)
    if os.path.exists(fp):
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND (former county): {filename}")

print("\nDone! Remaining profiles updated.")
