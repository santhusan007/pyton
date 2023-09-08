const puppeteer = require('puppeteer')
const cheerio = require('cheerio')

const {
  errors,
  constants: {
    locations: {
      USStates
    }
  }
} = require('by-lib')

const {
  randomWait,
  navigateToPage,
  arrayClean,
  slowType
} = require('~/utils')

const SITE_ROOT_URL = 'https://www.abcxyz.com'

async function search (ctx, data) {
  const browser = await puppeteer.launch({ headless: false }) // default is true
  const page = await browser.newPage()
  await navSearchPage(page, data.privateInfo)
  await randomWait(500, 1000)
  await fillSearchForm(page, data)
  const response = await submitSearchForm(page, data.privateInfo)
  await randomWait()
 
  const records = await extractRecords(page, response)

  return {
    message: '',
    records
  }
}

// --------------------------------------------------------------
//  Layers
// --------------------------------------------------------------

/*
async function navSearchPage (page, { firstName, middleInitial, lastName,city, state }) {  
  const name = middleInitial.length > 0 ? `${firstName} ${middleInitial} ${lastName}` : `${firstName} ${lastName}`
  const link = `${SITE_ROOT_URL}/people/${name}/${city},${state}`
  console.log(link)
  return await navigateToPage(page, { link }, { waitUntil: 'networkidle2', referrer: SITE_ROOT_URL })
}*/

async function navSearchPage (page) {  
  await navigateToPage(page, { link: SITE_ROOT_URL }, { referer: SITE_ROOT_URL })
}

async function fillSearchForm (page, data) {
  try {
    
    const {firstName, middleInitial, lastName,city, state} = data.privateInfo
    console.log("data",firstName, middleInitial, lastName,city, state);
    const name = middleInitial.length > 0 ? `${firstName} ${middleInitial} ${lastName}` : `${firstName} ${lastName}`
    if (await page.$('#person-name') === null) {
      console.warn('No Filter found')
    }
    await slowType(page, '#person-name', name)
    await slowType(page,'#person-location', `${city},${state}`)
   
  } catch (err) {
    // this shouldn't prevent us from getting results, just log it
    console.warn(`Could not find filter - ${err}`)
  }
}

async function submitSearchForm (page, { firstName, middleInitial, lastName,city, state }) {
  const name = middleInitial.length > 0 ? `${firstName} ${middleInitial} ${lastName}` : `${firstName} ${lastName}`
  const link = `${SITE_ROOT_URL}/people/${name}/${city},${state}`
  console.log(link)
  return await navigateToPage(page, { link }, { waitUntil: 'networkidle2', referrer: SITE_ROOT_URL })
}


async function extractRecords (page) {
  if (await page.$('section.mb-5').length === null) {
    throw new errors.NoMatchingRecords()
  }

  const content = await page.$eval('main', element => element.innerHTML)
  const $ = cheerio.load(content)
  const rows = $('section.mb-5')

  const records = []
  for (let i = 0; i < rows.length; i++) {
    const row = rows.eq(i)

    let age = ''
    const addresses = []
    const relatives = []

    row.find('ul.list-unstyled li').each(function (index, data) {
      const detailRow = $(data).text()

      if (detailRow.includes('Age')) {
        age = $(data).find('span').text()
      }

      if (detailRow.includes('Lives in')) {
        addresses.push($(data).find('span').text())
      }

      if (detailRow.includes('Related to')) {
        relatives.push($(data).find('span').text())
      }
    })


    records.push({
      index: i,
      fullName: $(row).find('h2 > span').text().trim(),
      age: age === '' ? 'available' : age,
      addresses: addresses.length > 0 ? arrayClean(addresses) : ['available'],
      relatives: relatives.length === 0 ? ['available'] : relatives,
      link: SITE_ROOT_URL+$(row).find('.btn-block').attr('href')
    })
  }
  console.log("all records found",records.length);
  console.log("all records found",records);
  return records
}

module.exports = search
module.exports.extractRecords = extractRecords
module.exports.navSearchPage = navSearchPage
module.exports.SITE_ROOT_URL = SITE_ROOT_URL

const ctx = { page: { _client: {}, keyboard: {}, response: {} } }
const privacyInfo = { privateInfo: { firstName: 'John', middleInitial: '', lastName: 'Smith', birthYear: 1932, addresses: [{ current: true, city: 'South Padre Island', state: 'TX' }], phoneNumbers: [], emailAddresses: [], city: 'South Padre Island', state: 'TX', minBirthYear: 1929, maxBirthYear: 1935, minBirthYearUnix: '-1293859800', maxBirthYearUnix: '-1073107800', age: 89, minAge: 86, maxAge: 92 } }

search(ctx, privacyInfo)
