import asyncio
import sys
from playwright.async_api import async_playwright
import random
from logfile import setup_logger

# Get the configured logger
logger = setup_logger()

async def fedex_courier_crawler(from_location,to_location,weight):
    logger.info(f'fedex_courier_crawler is started, file-name: fedex_courier_crawler.py,from {from_location}-to {to_location}')
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=["--start-fullscreen"]
            )
            context = await browser.new_context(no_viewport=True)
            page = await context.new_page()

            await page.goto('https://www.fedex.com/en-in/online/rating.html')
            logger.info('https://www.fedex.com/en-in/online/rating.html')
            # Accept cookie
            await page.wait_for_selector('#accept')
            await page.click('#accept')


            # Fill from address
            await page.click('#fromGoogleAddress')
            await page.fill('#fromGoogleAddress', from_location)
            await page.click('#e2eGoogleAddressSuggestionList .fdx-c-icon')

            # Fill to address
            await page.click('#toGoogleAddress')
            await page.fill('#toGoogleAddress',to_location)
            await page.click('#e2eGoogleAddressSuggestionList .fdx-c-icon')

            try:
                if to_location.lower() in 'united kingdom':  
                    await page.click('#toPostcode')  # focus input
                    await page.fill('#toPostcode', 'SW1A0RS')
                    #for x in range(0,2):
                    box = await page.locator('#toPostcode').bounding_box()
                    await page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                    await page.wait_for_timeout(300 + random.randint(0, 200))  # small delay
                    await page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2, button='left')
                    await page.click('xpath=//*[@id="main-container"]/div/fdx-common-core/fdx-loading-indicator/div[2]/div/div/div/magr-error/magr-locations-container/magr-error/fieldset/magr-error/div/button')
                    logger.info(f'found  input field for postal code and cilcked to continue,file-name: fedex_courier_crawler.py,{from_location}-{to_location}')
            except:
                pass
            # Select package type
            await page.locator('#package-details__package-type .fdx-c-icon').click(force=True)
            if int(weight)<=1:
                await page.select_option('#package-details__package-type select', value='FEDEX_BOX',timeout=10000)
            elif int(weight)>1 and int(weight)<=10:
                await page.select_option('#package-details__package-type select', value='FEDEX_10KG_BOX',timeout=10000)
            elif int(weight)>10:
                await page.select_option('#package-details__package-type select', value='FEDEX_25KG_BOX',timeout=10000)


            # Fill weight
            await page.locator('#package-details__weight-0 .fdx-c-form__input').click()
            await page.fill('#package-details__weight-0 .fdx-c-form__input', weight) 

            # Submit form to get rates
            await page.click('#e2ePackageDetailsSubmitButtonRates')

            # Wait to view results (optional)
            cost=await page.locator('.magr-c-rates button .fdx-u-flex.fdx-u-flex--column').nth(0).inner_text()
            await browser.close()
            logger.info(f'got data form fedex website,file-name: fedex_courier_crawler.py,from {from_location}-to {to_location},fedex_rates={cost}')
            return {"status":"success","message": "fedex calculator run successfully", "data":{"rates": cost}}
        
    except Exception as e:
        logger.error(f'{str(e)},file-name: fedex_courier_crawler.py,from {from_location} -to {to_location}')
        return {"status":"error","message": str(e), "data":{}}
        

 
