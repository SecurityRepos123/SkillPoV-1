const axios = require("axios")
const cheerio = require("cheerio")

// Receive HTML data
async function fetchHTML(url) {
  const { data } = await axios.get(url)
  return cheerio.load(data)
}
const $ = await fetchHTML("https://www.worldometers.info/coronavirus/")

let data = [];
const table = $('#main_table_countries_today');
const tr = table.find('tbody').children();

// Build data object
for (let i=0; i<150; i++){

  if (tr[i]['children'][1]['children'][0]['type'] === 'tag'){
    const country = tr[i]['children'][1]['children'][0]['children'][0]['data'];
    const totalCases = tr[i]['children'][3]['children'][0]['data'];
    const deaths = tr[i]['children'][7]['children'][0]['data'].trim();
    let obj = { country, totalCases, deaths };
    data.push(obj);

  } else {

    const country = tr[i]['children'][1]['children'][0]['data'];
    const totalCases = tr[i]['children'][3]['children'][0]['data'];
    let deaths = tr[i]['children'][7]['children'][0]['data'].trim();
    if (deaths === ''){
      deaths = 'Not available'
    };
    let obj = { country, totalCases, deaths };
    data.push(obj);

}}

this.data = data
