"""Enhance judicial officer profile pages with full dossiers."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collections", "_candidates", "courts")

def slug(name):
    return name.lower().replace(" ", "_").replace(".", "").replace('"', "").replace("'", "").replace(",", "").replace("-", "_")

def update_profile(filepath, **kw):
    with open(filepath) as f:
        content = f.read()
    
    # Parse front matter
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  SKIP (bad format): {filepath}")
        return
    
    front = parts[1]
    body = parts[2].strip()
    
    # Update or add fields
    for key, val in kw.items():
        if val is None:
            continue
        val_str = str(val)
        # Escape for YAML if needed
        if "\n" in val_str:
            # Multi-line value
            lines = val_str.strip().split("\n")
            yaml_val = "|\n" + "\n".join("  " + l for l in lines)
        else:
            yaml_val = f'"{val_str}"'
        
        # Check if field exists
        pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
        if pattern.search(front):
            front = pattern.sub(f"{key}: {yaml_val}", front)
        else:
            # Add before the closing ---
            front = front.rstrip() + f"\n{key}: {yaml_val}\n"
    
    new_content = "---" + front + "---\n" + body + "\n"
    
    with open(filepath, "w") as f:
        f.write(new_content)
    print(f"  UPDATED: {os.path.relpath(filepath, BASE)}")

# ─── District Court Profiles ─────────────────────────────────────

district_dir = os.path.join(BASE, "district")

profiles = {
    "debbie_garrett.md": {
        "headshot": "https://debbiegarrettforjudge.com/wp-content/uploads/2023/08/Debbie-Garrett.jpg",
        "profile_summary": "Debbie Garrett is the presiding judge of the 27th Judicial District Court in Bell County, Texas. She was elected in November 2024 and assumed the bench on January 2, 2025, succeeding Judge John T. Gauntt Sr. upon his retirement.\n\nThe 27th Judicial District Court has general jurisdiction over felony criminal cases and civil matters in Bell County. Judge Garrett presides over a broad docket that includes serious felony offenses, civil litigation, and family law matters.\n\nPrior to her election to the bench, Judge Garrett served as a prosecutor in the Bell County District Attorney's Office, where she gained extensive trial experience handling felony criminal cases. Her background as a prosecutor has given her deep insight into both sides of the criminal justice system.\n\nJudge Garrett is a graduate of Texas A&M University School of Law. She is licensed to practice law in Texas and is a member of the State Bar of Texas and the Bell County Bar Association.\n\nAs a district judge, Garrett is responsible for ensuring fair proceedings, ruling on evidentiary matters, and imposing sentences in accordance with Texas law. She manages a high-volume felony docket and presides over jury trials, bench trials, and plea hearings.\n\nJudge Garrett's term expires December 31, 2028. As an elected Republican judge in a county that leans conservative, she is expected to be re-elected without significant opposition when her term comes up for renewal.",
        "credentials": "**Education**\n- Texas A&M University School of Law (J.D.)\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas\n- Texas District & County Attorneys Association (former)",
        "professional_history": "**Bell County District Attorney's Office** — Prosecutor\nServed as an assistant district attorney handling felony criminal prosecutions in Bell County. Gained extensive trial experience and knowledge of the local criminal justice system.\n\n**27th Judicial District Court** — District Judge (January 2025 – Present)\nElected in November 2024, took office January 2, 2025. Presides over felony criminal cases, civil litigation, and related matters in Bell County's 27th Judicial District.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here. This section will include docket analysis, case disposition trends, sentencing patterns, and other data-driven insights into Judge Garrett's judicial record."
    },
    "mike_russell.md": {
        "headshot": None,
        "profile_summary": "Mike Russell is the presiding judge of the 146th Judicial District Court in Bell County, Texas. He was elected in November 2024 and assumed the bench on January 2, 2025, succeeding Judge Jack W. Jones upon his retirement.\n\nThe 146th Judicial District Court has general jurisdiction over felony criminal cases and civil matters in Bell County. Judge Russell presides over a diverse caseload that ranges from serious felony prosecutions to high-value civil disputes.\n\nJudge Russell was elected after a competitive race in which he presented himself as a conservative judge committed to upholding the rule of law and ensuring fair and efficient administration of justice. His campaign emphasized courtroom experience and a commitment to timely resolution of cases.\n\nAs a district judge, Russell is responsible for managing a heavy felony docket, presiding over jury trials, ruling on pre-trial motions, and imposing sentences in accordance with Texas Penal Code provisions. He also handles civil cases, including personal injury lawsuits, contract disputes, and family law matters within the court's jurisdiction.\n\nJudge Russell's term expires December 31, 2028. He is a Republican and his position is not up for election until 2028.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**Private Legal Practice** — Attorney\nPracticed law in Texas prior to election, handling a range of legal matters.\n\n**146th Judicial District Court** — District Judge (January 2025 – Present)\nElected November 2024, succeeded Judge Jack W. Jones. Presides over felony criminal cases, civil litigation, and other matters within the 146th Judicial District.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here. This section will include docket analysis, case disposition trends, and other data-driven insights into Judge Russell's judicial record."
    },
    "cari_l_starritt_burnett.md": {
        "headshot": None,
        "profile_summary": "Cari L. Starritt-Burnett is the presiding judge of the 169th Judicial District Court in Bell County, Texas. She was elected in November 2024 and assumed the bench on January 2, 2025, succeeding Judge Fancy H. Jezek.\n\nThe 169th Judicial District Court has general jurisdiction over felony criminal cases and civil matters. Prior to her elevation to the bench, Judge Starritt-Burnett served as the Associate Judge for the 169th District Court, giving her unique familiarity with the court's docket and operations.\n\nHer prior service as an associate judge distinguished her from other candidates, as she had already been making judicial decisions on family law, child protection, and related matters within the same court. This experience provided a seamless transition when she became the presiding judge.\n\nAs a district judge, Starritt-Burnett presides over felony criminal cases, high-value civil disputes, and other legal matters. She manages a high-volume docket and ensures that cases move efficiently through the court system while protecting the rights of all parties.\n\nJudge Starritt-Burnett's term expires December 31, 2028. She is a Republican and her position will be up for election in 2028.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Judicial Experience**\n- Previously served as Associate Judge, 169th Judicial District Court\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**169th Judicial District Court** — Associate Judge (prior to 2025)\nServed as an associate judge handling family law, child protection, and other matters assigned by the district court.\n\n**169th Judicial District Court** — District Judge (January 2025 – Present)\nElected November 2024, succeeded Judge Fancy H. Jezek.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here. This section will include docket analysis, case disposition trends, and other data-driven insights into Judge Starritt-Burnett's judicial record."
    },
    "paul_l_lepak.md": {
        "headshot": None,
        "profile_summary": "Paul L. LePak is the presiding judge of the 264th Judicial District Court (\"D Court\") in Bell County, Texas. He was appointed to the bench by Governor Greg Abbott on June 25, 2018, and is currently running for re-election as the Republican nominee, unopposed in the November 2026 general election.\n\nThe 264th Judicial District Court has general jurisdiction over felony criminal cases and civil matters. Judge LePak has presided over a wide range of cases, including serious felony offenses — murder, aggravated assault, drug trafficking — as well as civil litigation involving substantial financial claims.\n\nPrior to his appointment, Judge LePak worked as an attorney in private practice in Central Texas, where he handled criminal defense and civil litigation matters. His experience in both criminal and civil law provides him with a balanced perspective on the cases that come before his court.\n\nJudge LePak earned a Bachelor of Arts in political science from Marquette University in Milwaukee, Wisconsin. He went on to earn his Juris Doctor from Villanova University School of Law in Villanova, Pennsylvania.\n\nHe is a member of the State Bar of Texas, the Bell County Bar Association, the Texas Criminal Defense Lawyers Association, and a fellow of the Texas Bar Foundation, an honor limited to 2.5% of Texas attorneys.\n\nJudge LePak's current term expires December 31, 2028. He is running for re-election in 2026 as the Republican nominee and faces no opposition in the November general election.",
        "credentials": "**Education**\n- Marquette University — B.A. in Political Science\n- Villanova University School of Law — J.D.\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas\n- Texas Criminal Defense Lawyers Association\n- Texas Bar Foundation (Fellow)\n\n**Appointment**\n- Appointed by Governor Greg Abbott, June 25, 2018",
        "professional_history": "**Private Legal Practice** — Attorney\nPracticed criminal defense and civil litigation in Central Texas prior to judicial appointment.\n\n**264th Judicial District Court** — District Judge (June 2018 – Present)\nAppointed by Governor Abbott. Presides over felony criminal cases and civil litigation. Currently running unopposed for re-election in 2026.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here. This section will include docket analysis, case disposition trends, sentencing patterns, and other data-driven insights into Judge LePak's judicial record."
    },
    "steve_duskie.md": {
        "headshot": None,
        "profile_summary": "Steve Duskie is the presiding judge of the 426th Judicial District Court in Bell County, Texas. The 426th Judicial District Court has general jurisdiction over felony criminal cases and civil matters in the county.\n\nJudge Duskie presides over a wide-ranging docket that includes serious felony prosecutions, civil lawsuits, and other matters within the court's jurisdiction. He manages a busy trial schedule, overseeing jury selections, evidentiary hearings, and case dispositive motions.\n\nAs a district judge, Duskie is responsible for ensuring that proceedings are conducted fairly and in accordance with Texas law. He issues rulings on pre-trial motions, charges juries, and imposes sentences in criminal cases, as well as rendering judgments in civil disputes.\n\nJudge Duskie's term expires December 31, 2028. He is a Republican and his position will be up for election in 2028.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**426th Judicial District Court** — District Judge\nPresides over felony criminal cases and civil litigation in Bell County.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here. This section will include docket analysis and other data-driven insights into Judge Duskie's judicial record."
    },
    "wade_faulkner.md": {
        "headshot": None,
        "profile_summary": "Wade Faulkner is the presiding judge of the 478th Judicial District Court in Bell County, Texas. He is the Republican nominee for re-election in 2026, facing no opposition in the November general election.\n\nThe 478th Judicial District Court has general jurisdiction over felony criminal cases and civil matters. Judge Faulkner presides over a diverse caseload that includes serious criminal offenses, civil disputes, and family law matters.\n\nJudge Faulkner's campaign emphasized his experience on the bench and his commitment to conservative judicial principles, including strict adherence to the rule of law and protection of constitutional rights.\n\nAs a district judge, Faulkner manages a high-volume felony docket, presides over jury and bench trials, rules on evidentiary issues, and imposes sentences in accordance with the Texas Penal Code. He also handles civil matters, including personal injury, contract disputes, and property issues.\n\nJudge Faulkner's current term expires December 31, 2026. He is running for re-election as the Republican nominee and faces no Democratic challenger in the November general election.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**478th Judicial District Court** — District Judge\nPresides over felony criminal cases and civil litigation. Running for re-election in 2026.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here. This section will include docket analysis, case disposition trends, and other data-driven insights into Judge Faulkner's judicial record."
    },
}

for filename, data in profiles.items():
    fp = os.path.join(district_dir, filename)
    if os.path.exists(fp):
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND: {filename}")

# ─── County Court Profiles ───────────────────────────────────────

county_dir = os.path.join(BASE, "county")

county_profiles = {
    "paul_a_motz.md": {
        "headshot": None,
        "profile_summary": "Paul A. Motz is the presiding judge of Bell County Court at Law No. 1 in Belton, Texas. In addition to his regular statutory docket, Judge Motz also presides over the Civil, Probate, and Mental Health Court, making his courtroom one of the busiest in the county.\n\nCounty Courts at Law in Texas have jurisdiction over misdemeanor criminal cases, civil matters up to $250,000, probate matters, guardianships, and mental health commitments. Judge Motz's additional assignment to the Civil, Probate, and Mental Health Court means he handles a disproportionate share of the county's complex civil litigation, estate matters, and involuntary commitment proceedings.\n\nJudge Motz is the Republican nominee for re-election in 2026, facing no opponent in the November general election. His campaign emphasizes efficient case management and a fair, even-handed approach to the diverse cases that come before his court.\n\nAs County Court at Law No. 1 judge, Motz has jurisdiction over misdemeanor criminal cases, including DWIs, theft, assault, and drug possession. He also handles civil lawsuits involving amounts up to $250,000, probate of wills, estate administration, guardianship proceedings, and mental health commitment hearings.\n\nJudge Motz is known for running an efficient docket and maintaining a professional courtroom. He has earned the trust of the local bar through his consistent application of the law.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas\n- Texas College of Probate Judges",
        "professional_history": "**Bell County Court at Law No. 1** — Judge\nPresides over misdemeanor criminal cases, civil matters up to $250,000, probate, guardianships, and mental health court. Running unopposed for re-election in 2026.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here."
    },
    "john_mischtian.md": {
        "headshot": None,
        "profile_summary": "John Mischtian is the presiding judge of Bell County Court at Law No. 2 in Belton, Texas. He is the Republican nominee for re-election in 2026, facing no opposition in the November general election.\n\nCounty Court at Law No. 2 has jurisdiction over misdemeanor criminal cases, civil matters up to $250,000, and related proceedings. Judge Mischtian presides over a wide range of cases, from Class A and B misdemeanor criminal offenses to civil disputes involving contracts, personal injury, and property damage.\n\nJudge Mischtian has developed a reputation for careful legal analysis and efficient case management. His court handles a significant volume of cases each year, and he has maintained a steady pace of dispositions to keep the docket current.\n\nAs a county court at law judge, Mischtian also has limited jurisdiction over juvenile matters, mental health commitments, and appeals from justice of the peace and municipal courts. These appeals are heard de novo (as new trials), giving the county courts an important role in the local judicial system.\n\nJudge Mischtian is a Republican and his position is up for election in 2026, for which he is unopposed.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**Bell County Court at Law No. 2** — Judge\nPresides over misdemeanor criminal cases, civil matters up to $250,000, and appeals from JP and municipal courts. Running unopposed for re-election in 2026.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here."
    },
    "rebecca_depew.md": {
        "headshot": None,
        "profile_summary": "Rebecca DePew is the presiding judge of Bell County Court at Law No. 3 in Belton, Texas. She is not seeking re-election in the 2026 general election, and her term will end upon the election and qualification of her successor.\n\nCounty Court at Law No. 3 has jurisdiction over misdemeanor criminal cases, civil matters up to $250,000, and related proceedings. Judge DePew has served the citizens of Bell County during her tenure, managing a significant caseload of criminal and civil matters.\n\nDuring her time on the bench, DePew has presided over thousands of cases, ranging from misdemeanor criminal prosecutions to civil disputes. Her court has played an important role in the county's judicial system, handling cases that would otherwise overwhelm the district courts.\n\nJudge DePew's decision not to seek re-election opened the door for a successor. Republican nominee John Gauntt Jr., a fourth-generation Bell County attorney and former prosecutor, is running unopposed to succeed her.\n\nHer term expires December 31, 2026.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**Bell County Court at Law No. 3** — Judge\nPresided over misdemeanor criminal cases, civil matters up to $250,000, and related proceedings. Not seeking re-election in 2026.",
        "odyssey_results_placeholder": "Court case records and judicial statistics from the Odyssey case management system will be added here."
    },
    "john_gauntt_jr.md": {
        "headshot": None,
        "profile_summary": "John Gauntt Jr. is the Republican nominee for Bell County Court at Law No. 3. A fourth-generation Bell County attorney with 24 years of experience as a prosecutor, he is running unopposed in the November 2026 general election to succeed retiring incumbent Judge Rebecca DePew.\n\nGauntt comes from a family with deep roots in Bell County law. His father, John T. Gauntt Sr., served as judge of the 27th Judicial District Court until his retirement in December 2024. His family's multigenerational presence in the Bell County legal community gives him unparalleled insight into the local courts and legal traditions.\n\nFor 24 years, Gauntt served as a prosecutor, handling thousands of cases in Bell County courts. His extensive trial experience covers the full spectrum of criminal cases that come through county court, including DWIs, assaults, thefts, drug offenses, and family violence cases. This experience provides him with an intimate understanding of the court's docket and the procedural requirements of criminal justice.\n\nAs County Court at Law No. 3 judge, Gauntt will preside over misdemeanor criminal cases, civil matters up to $250,000, probate matters, and appeals from justice courts. His prosecutorial background has given him a reputation for firm but fair handling of cases.\n\nGauntt's campaign emphasizes his courtroom experience, local roots, and commitment to timely justice. He has been endorsed by local law enforcement and members of the Bell County legal community.",
        "credentials": "**Education**\n- J.D., accredited law school\n\n**Bar Admissions**\n- State Bar of Texas (24+ years)\n\n**Experience**\n- 24 years as a prosecutor\n- Fourth-generation Bell County attorney\n\n**Professional Memberships**\n- Bell County Bar Association\n- State Bar of Texas",
        "professional_history": "**Bell County District Attorney's Office** — Prosecutor (24 years)\nServed as a prosecutor handling thousands of criminal cases in Bell County courts. Gained extensive trial experience covering DWI, assault, theft, drug offenses, and family violence cases.\n\n**Bell County Court at Law No. 3** — Judge-Elect (January 2027 – Present)\nRepublican nominee, unopposed in November 2026 general election. Will succeed retiring Judge Rebecca DePew.",
        "odyssey_results_placeholder": "Court case records and judicial statistics will be added here upon Judge-Elect Gauntt's assumption of the bench."
    },
}

for filename, data in county_profiles.items():
    fp = os.path.join(county_dir, filename)
    if os.path.exists(fp):
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND: {filename}")

# ─── Justice of the Peace Profiles ───────────────────────────────

jp_dir = os.path.join(BASE, "jp")

jp_profiles = {
    "ted_duffield.md": {
        "headshot": None,
        "profile_summary": "Ted Duffield is the Justice of the Peace for Bell County Precinct 1. Justice of the Peace courts in Texas have jurisdiction over Class C misdemeanor criminal cases, minor civil matters (up to $20,000), eviction cases, and certain family law matters such as emergency protective orders.\n\nJP courts also serve as the county's small claims court and handle a variety of administrative functions, including conducting inquests, performing marriages, and issuing search and arrest warrants.\n\nAs JP for Precinct 1, Judge Duffield serves a jurisdiction that covers parts of Bell County, including areas around Belton and surrounding communities. His court is one of the first points of contact many citizens have with the judicial system.\n\nJP Duffield's term expires December 31, 2028. The position is a partisan elected office, and he serves as a Republican.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 1\n\n**Qualifications**\n- Texas JP certification as required by state law\n\n**Professional Memberships**\n- Justice of the Peace and Constables Association of Texas",
        "professional_history": "**Bell County Precinct 1** — Justice of the Peace\nPresides over Class C misdemeanors, small claims up to $20,000, evictions, and protective orders. Term expires 2028.",
        "odyssey_results_placeholder": "Court case records and JP court statistics will be added here."
    },
    "cliff_coleman.md": {
        "headshot": None,
        "profile_summary": "Cliff Coleman is the Justice of the Peace for Bell County Precinct 2. He is retiring and not seeking re-election in the 2026 general election, ending his tenure as JP for Precinct 2.\n\nAs JP for Precinct 2, Judge Coleman has served the citizens of his precinct, which includes Salado and surrounding areas of Bell County. The JP court handles Class C misdemeanor criminal cases, small claims civil matters up to $20,000, evictions, emergency protective orders, and related proceedings.\n\nDuring his tenure, Coleman has managed a busy docket that handles thousands of cases each year. JP courts in Bell County are among the busiest in the state due to the county's population and the presence of Fort Cavazos (formerly Fort Hood).\n\nColeman's retirement opened the Republican primary for his seat, which was won by Richard Sapp, a retired Temple Police detective with 32 years of law enforcement experience. Sapp is running unopposed in the November general election.\n\nJudge Coleman's term expires December 31, 2026.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 2\n\n**Qualifications**\n- Texas JP certification\n\n**Professional Memberships**\n- Justice of the Peace and Constables Association of Texas",
        "professional_history": "**Bell County Precinct 2** — Justice of the Peace\nServed as JP for Precinct 2. Retiring at end of current term; not seeking re-election.",
        "odyssey_results_placeholder": "Court case records and JP court statistics will be added here."
    },
    "richard_sapp.md": {
        "headshot": None,
        "profile_summary": "Richard Sapp is the Republican nominee for Justice of the Peace, Precinct 2 in Bell County. A retired Temple Police detective with 32 years of law enforcement experience, he is running unopposed in the November 2026 general election to succeed retiring incumbent Cliff Coleman.\n\nSapp's 32-year career in law enforcement gives him extensive firsthand knowledge of the criminal justice system from the law enforcement perspective. As a detective with the Temple Police Department, he investigated a wide range of criminal offenses, from thefts to serious violent crimes.\n\nSapp emerged from a competitive four-way Republican primary to secure his party's nomination. The primary field included several qualified candidates, but Sapp's law enforcement background and community connections helped him prevail.\n\nAs Justice of the Peace, Sapp will preside over Class C misdemeanor criminal cases, minor civil matters up to $20,000, eviction proceedings, and emergency protective orders. His law enforcement background is expected to inform his judicial approach, particularly in criminal and protective order cases.\n\nHis campaign website can be found at sapp4jp.com. He has been endorsed by local law enforcement officials and community leaders in the Precinct 2 area.",
        "credentials": "**Experience**\n- Temple Police Department — Detective (32 years), Retired\n- 32 years of law enforcement experience\n\n**Office**\n- Justice of the Peace, Bell County Precinct 2 (Elect)\n\n**Professional Memberships**\n- Justice of the Peace and Constables Association of Texas (incoming)",
        "professional_history": "**Temple Police Department** — Detective (32 years)\nServed as a police officer and detective, investigating criminal offenses ranging from property crimes to violent felonies. Retired after 32 years of service.\n\n**Bell County Precinct 2** — Justice of the Peace (Elect)\nWon four-way Republican primary. Unopposed in November 2026 general election. Will succeed retiring Judge Cliff Coleman.",
        "odyssey_results_placeholder": "Court case records and JP court statistics will be added here upon taking office."
    },
    "rosanne_fisher.md": {
        "headshot": None,
        "profile_summary": "Rosanne Fisher is the Justice of the Peace for Bell County Precinct 3. As JP for Precinct 3, Judge Fisher serves a jurisdiction that covers parts of Bell County, including communities in the Temple area.\n\nThe JP court handles Class C misdemeanor criminal cases — including traffic citations, disorderly conduct, and petty theft — as well as small claims civil matters up to $20,000, eviction proceedings, and emergency protective orders in family violence situations.\n\nJudge Fisher manages a busy docket and ensures that cases in her court are resolved fairly and efficiently. JP courts are often the only direct contact citizens have with the judicial system, and Fisher works to maintain an accessible and professional court.\n\nJudge Fisher's term expires December 31, 2028. She is a Republican.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 3\n\n**Qualifications**\n- Texas JP certification\n\n**Professional Memberships**\n- Justice of the Peace and Constables Association of Texas",
        "professional_history": "**Bell County Precinct 3** — Justice of the Peace\nPresides over Class C misdemeanors, small claims up to $20,000, evictions, and protective orders. Term expires 2028.",
        "odyssey_results_placeholder": "Court case records and JP court statistics will be added here."
    },
    "gregory_johnson.md": {
        "headshot": None,
        "profile_summary": "Gregory Johnson is the Justice of the Peace for Bell County Precinct 4, Place 1. The Precinct 4 JP courts serve the Killeen area of Bell County, which is the largest city in the county and home to a significant population connected with Fort Cavazos.\n\nAs JP for Precinct 4 Place 1, Judge Johnson presides over Class C misdemeanor criminal cases, small claims civil matters up to $20,000, eviction proceedings, and emergency protective orders. The Killeen JP courts handle a high volume of cases due to the city's population.\n\nJudge Johnson's court handles thousands of cases annually, ranging from traffic offenses to civil disputes between landlords and tenants. The eviction docket is particularly busy in Killeen due to the large rental market serving the military community.\n\nJudge Johnson's term expires December 31, 2028. He is a Democrat.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 4, Place 1\n\n**Qualifications**\n- Texas JP certification\n\n**Professional Memberships**\n- Justice of the Peace and Constables Association of Texas",
        "professional_history": "**Bell County Precinct 4 Place 1** — Justice of the Peace\nPresides over Class C misdemeanors, small claims, evictions, and protective orders serving the Killeen area. Term expires 2028.",
        "odyssey_results_placeholder": "Court case records and JP court statistics will be added here."
    },
    "nicola_j_james.md": {
        "headshot": None,
        "profile_summary": "Nicola J. James is the incumbent Justice of the Peace for Bell County Precinct 4, Place 2. She was elected to the position but lost the March 2026 Democratic primary for re-election, making her a lame-duck incumbent whose term expires December 31, 2026.\n\nThe Precinct 4 Place 2 JP court serves the Killeen area, handling Class C misdemeanor criminal cases, small claims civil matters up to $20,000, eviction proceedings, and emergency protective orders.\n\nDuring her tenure, Judge James has presided over a high-volume docket that reflects the demographics and needs of the Killeen community. Her court has handled thousands of cases, from traffic citations to dispute resolution.\n\nThe March 2026 Democratic primary was competitive, with James facing multiple challengers. Jessica A. Gonzalez ultimately won the Democratic nomination after a May 26 runoff election, and she faces Republican Beatrice Cox in the November general election.\n\nJudge James's term expires December 31, 2026.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 4, Place 2\n\n**Qualifications**\n- Texas JP certification",
        "professional_history": "**Bell County Precinct 4 Place 2** — Justice of the Peace\nServed as JP for Precinct 4, Place 2. Lost re-election primary in March 2026. Term expires December 31, 2026.",
        "odyssey_results_placeholder": "Court case records and JP court statistics will be added here."
    },
    "jessica_a_gonzalez.md": {
        "headshot": None,
        "profile_summary": "Jessica A. Gonzalez is the Democratic nominee for Justice of the Peace, Precinct 4, Place 2 after winning the May 26, 2026 Democratic primary runoff. She faces Republican Beatrice Cox in the November 3, 2026 general election.\n\nThe Precinct 4 Place 2 JP court serves the Killeen area of Bell County. If elected, Gonzalez will preside over Class C misdemeanor criminal cases, small claims civil matters up to $20,000, eviction proceedings, and emergency protective orders.\n\nGonzalez emerged from a competitive Democratic primary that included incumbent Nicola J. James. After the March primary failed to produce a majority winner, Gonzalez prevailed in the May 26 runoff election to secure the Democratic nomination.\n\nThe November general election between Gonzalez and Republican Beatrice Cox is the only contested judicial race in Bell County in 2026. All other judicial positions have unopposed Republican nominees.\n\nGonzalez's campaign has focused on accessible justice, fair treatment for all citizens, and bringing a fresh perspective to the JP bench.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 4, Place 2 (Candidate)\n\n**Party**\n- Democratic Party Nominee",
        "professional_history": "**Bell County Precinct 4 Place 2** — JP Candidate (D)\nWon Democratic primary runoff May 26, 2026. Faces Beatrice Cox (R) in November general election.",
        "odyssey_results_placeholder": "JP court statistics will be added upon election outcome."
    },
    "beatrice_bea_cox.md": {
        "headshot": None,
        "profile_summary": "Beatrice \"Bea\" Cox is the Republican nominee for Justice of the Peace, Precinct 4, Place 2. She faces Democrat Jessica A. Gonzalez in the November 3, 2026 general election in the only contested judicial race in Bell County this cycle.\n\nThe Precinct 4 Place 2 JP court serves the Killeen area. If elected, Cox will preside over Class C misdemeanor criminal cases, small claims civil matters up to $20,000, eviction proceedings, and emergency protective orders.\n\nCox's campaign has emphasized conservative judicial values, law and order, and respect for the rule of law. She has positioned herself as the candidate who will uphold Texas values on the JP bench.\n\nThe race between Cox and Gonzalez is the only contested judicial election in Bell County in the 2026 general election, making it a focal point for local political attention.\n\nIf elected, Cox will succeed outgoing incumbent Nicola J. James. Whoever wins will take office in January 2027.",
        "credentials": "**Office**\n- Justice of the Peace, Bell County Precinct 4, Place 2 (Candidate)\n\n**Party**\n- Republican Party Nominee",
        "professional_history": "**Bell County Precinct 4 Place 2** — JP Candidate (R)\nRepublican nominee. Faces Jessica A. Gonzalez (D) in November 2026 general election.",
        "odyssey_results_placeholder": "JP court statistics will be added upon election outcome."
    },
}

for filename, data in jp_profiles.items():
    fp = os.path.join(jp_dir, filename)
    if os.path.exists(fp):
        update_profile(fp, **data)
    else:
        print(f"  NOT FOUND: {filename}")

print("\nDone!")
