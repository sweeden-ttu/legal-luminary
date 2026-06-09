const https = require('https');
const fs = require('fs');
const path = require('path');

const url = 'https://www.allsides.com/api/search?searchText=texas+governor&page=0&type=roundups&searchMode=allsides';

const options = {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Cookie': '__cflb=0H28vy6QmJWTVYu6o6eVnreCJcJZXnpyYpnap9LRZiC; __eoi=ID=0b028786aea16eb1:T=1780690009:RT=1780690319:S=AA-AfjYCV97o3j5SaCJiMJoQXbUc; __gads=ID=32234e6da30d25a9:T=1780690009:RT=1780690319:S=ALNI_Ma6hWGl1ng1M_okEqU8nSMV1sKsMg; __gpi=UID=000013bc824c2a73:T=1780690009:RT=1780690319:S=ALNI_MYRcDTxKx4bHsxfstII_p2ltvrWuQ; __gsas=ID=cf3c58bc4d12092f:T=1780690247:RT=1780690247:S=ALNI_MZudE1rbNtegdBiF3uBkSFTV-GNbQ; _cc_id=fafd31f68b2ecb71d11ad0037d53e66e; _cfuvid=99wAvGeBZOKwaKCpxQCTkjEFmce0TIE_QXoTNbrgyk8-1780690004.6980007-1.0.1.1-r3CPbaV65IOZ1_TwMi8HSlNTXsdyZde24qCxXX1abgk; _ga=GA1.1.445904814.1780690005; _ga_097Z15EHGT=GS2.1.s1780690005$o1$g1$t1780690370$j36$l0$h0; _lc2_fpi=0a6f57a5ccad--01ktcpacdmmce05vk6ptzsw3qv; _li_dcdm_c=.allsides.com; cf_clearance=9zOAjQJYAvwoEOnNdmX0xp9e.DhO28oiq4T0vZj2s0A-1780690005-1.2.1.1-3fxkkThPn_dZ5pg9bMwAqKdfaLb0pB_2ettI4tgNxK.5GfTsf1TDzyuoI3n5hz9Es.bFNL6b3ZGB2C_9Tas.B3iLHq7i5GthxIFOM9mAV6hqweNn9I.rwMRH7D2uQj.PzdMZL0BJCajHFdoOewoM..DSpnOe7wCbPgDLakuC.R1PZIKh1Frwv2fMmYPMjbT2m9za8hKSdV_Do7GnWM08ehmDiWCZm29QHpdw5SI2qEWgjVQifyyLxE7JK42ibyIXwAWW4Ujiz8rhOpi.jCWIQR7smtTNdvhc4e5M99E.Lw9n.zK13UcUpyR5Unery7EfReAR10MI9IXqEP0CPLL58g'
  }
};

https.get(url, options, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      const filePath = path.join(__dirname, 'assets', 'data', 'texas_governor_news.json');
      fs.writeFileSync(filePath, JSON.stringify(json, null, 2));
      console.log('Successfully updated texas_governor_news.json');
    } catch (e) {
      console.error('Error parsing JSON:', e);
    }
  });

}).on('error', (e) => {
  console.error('Error fetching data:', e);
});
