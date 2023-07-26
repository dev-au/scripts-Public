#<Manba bilan tarqating: t.me/pycyberuz>#
#بِسْمِ ٱللَّٰهِ, #

class MovieGoer:
    import requests
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By
    driver = webdriver.Chrome()

    class SerializeResults:
        name: str
        url: str

        def __init__(self, name: str, url: str):
            self.name = name
            self.url = url

    results: list
    end_place: int

    search_name: str
    page_number: int

    def __init__(self, search_name, page_number: int = 1):
        self.search_name = search_name
        self.page_number = page_number
        search_result = self.search_movies()
        self.results = search_result[0]
        self.end_place = search_result[1]

    def get_url(self):
        main_url = "https://uzmovi.com/"
        if self.page_number == 1:
            control_url = "search?q="
            ready_url = f"{main_url}{control_url}{self.search_name}"
            return ready_url
        else:
            control_url = f"search/page/{self.page_number}?q="
            ready_url = f"{main_url}{control_url}{self.search_name}"
            return ready_url

    def search_movies(self):
        url = self.get_url()
        self.driver.get(url)
        resp = self.driver.find_element(self.By.ID, "mainbar")
        resp = resp.find_element(self.By.CLASS_NAME, "row")
        resp = resp.find_element(self.By.CLASS_NAME, "row")
        movie_urls = resp.find_elements(self.By.CLASS_NAME, "short-link")
        movies = []
        serializer = self.SerializeResults
        for movie_url in movie_urls:
            elements = str(movie_url.find_element(self.By.TAG_NAME, "a").get_attribute("outerHTML"))
            name: str = elements[elements.index(">") + 1:-4].strip()
            url: str = elements[9:(elements[9:].index("\"")) + 9].strip()
            movies.append(serializer(name, url))
        try:
            resp = resp.find_element(self.By.CLASS_NAME, "pages-numbers")
            end_place: int = int(resp.find_elements(self.By.TAG_NAME, "a")[-1].text.strip())
        except self.NoSuchElementException:
            end_place: int = 1
        return [movies, end_place]

    def download_movie(self, video_ser: SerializeResults):
        self.driver.get(video_ser.url)
        resp = self.driver.find_elements(self.By.CLASS_NAME, "btn1")
        if len(resp) == 1:
            link = resp[0].get_attribute("outerHTML")
            download_link = link[22:link.index(">") - 1]
            print("Downloading...")
            try:
                movie = self.requests.get(download_link, allow_redirects=True)
                print("Saving...")
                open(f"{video_ser.name}.mp4", 'wb').write(movie.content)
                print("Successfully downloaded!")
            except:
                print("Download stopped!")
                pass
        else:
            for rs in resp:
                print(rs)
            select = int(input("Qaysi sifat turini tanllaysiz sifat darajasi pasayib boradi")) - 1
            link = resp[select].get_attribute("outerHTML")
            download_link = link[22:link.index(">") - 1]
            try:
                movie = self.requests.get(download_link, allow_redirects=True)
                print("Saving...")
                open(f"{video_ser.name}.mp4", 'wb').write(movie.content)
                print("Successfully downloaded!")
            except:
                print("Download stopped!")
                pass

    def driver_close(self):
        self.driver.close()


movie_name = input("Film qidirng: ")
moviegoer = MovieGoer(search_name=movie_name, page_number=1)
search_results = moviegoer.results
end_page = moviegoer.end_place
for result in search_results:
    print(f"{result.name}  :  {result.url}\n")
print(f"Oxirgi sahifa: {end_page}")
select = int(input("Bo'lim tanlang: "))
moviegoer.download_movie(search_results[select - 1])
moviegoer.driver_close()
