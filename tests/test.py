from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import ETimeFilterOptions
from linkedin_jobs_scraper.events import Events, Data


def get_default_chrome_options(width=1472, height=828) -> Options:
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.page_load_strategy = 'normal'

    chrome_options.add_argument('--remote-debugging-address=0.0.0.0'),
    chrome_options.add_argument('--remote-debugging-port=9222'),

    chrome_options.add_argument('--enable-automation'),
    chrome_options.add_argument('--start-maximized'),
    chrome_options.add_argument(f'--window-size={width},{height}'),
    chrome_options.add_argument('--lang=en-GB'),
    chrome_options.add_argument('--no-sandbox'),
    chrome_options.add_argument('--disable-setuid-sandbox'),
    chrome_options.add_argument('--disable-gpu'),
    chrome_options.add_argument('--disable-dev-shm-usage'),
    chrome_options.add_argument('--no-sandbox'),
    chrome_options.add_argument('--disable-setuid-sandbox'),
    chrome_options.add_argument('--disable-dev-shm-usage'),
    chrome_options.add_argument("-proxy-server='direct://"),
    chrome_options.add_argument('--proxy-bypass-list=*'),
    chrome_options.add_argument('--disable-accelerated-2d-canvas'),
    chrome_options.add_argument('--disable-gpu'),
    chrome_options.add_argument('--allow-running-insecure-content'),
    chrome_options.add_argument('--disable-web-security'),
    chrome_options.add_argument('--disable-client-side-phishing-detection'),
    chrome_options.add_argument('--disable-notifications'),
    chrome_options.add_argument('--mute-audio'),

    # Disable downloads
    chrome_options.add_experimental_option(
        'prefs', {
            'safebrowsing.enabled': 'false',
            'download.prompt_for_download': False,
            'download.default_directory': '/dev/null',
            'download_restrictions': 3,
            'profile.default_content_setting_values.notifications': 2,
        }
    )

    return chrome_options


def build_chrome_driver(options: Options = None, timeout=20) -> webdriver:
    if options is not None:
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(options=get_default_chrome_options())

    driver.set_page_load_timeout(timeout)
    return driver


scraper = LinkedinScraper(driver_builder=build_chrome_driver)


def on_data(data):
    print(
        Events.DATA.value,
        data.title,
        data.company,
        len(data.link),
        len(data.apply_link),
        data.date,
        len(data.description),
        len(data.description_html),
        data.senority_level,
        data.job_function,
        data.employment_type,
        data.industries
    )

    with open('/Users/ludovicofabbri/Documents/Projects/python/py-linkedin-jobs-scraper/tests/output.txt', 'a') as file:
        line = '|'.join([
            str(data.query),
            str(data.location),
            str(data.place),
            str(data.title),
            str(data.company),
            str(len(data.link)),
            str(len(data.apply_link)),
            str(data.date),
            str(len(data.description)),
            str(len(data.description_html)),
            str(data.senority_level),
            str(data.job_function),
            str(data.employment_type),
            str(data.industries),
        ]) + '\n'

        file.write(line)


scraper.on(Events.DATA.value, on_data)
scraper.on(Events.ERROR.value, lambda error: print(Events.ERROR.value, error))
scraper.on(Events.END.value, lambda: print(Events.END.value))

queries = [
    Query(query='Software engineer', options=QueryOptions(limit=50, locations=['Rome', 'Paris'])),
    Query(options=QueryOptions(limit=100, filters=QueryFilters(time=ETimeFilterOptions.MONTH)))
]

scraper.run(queries=queries)