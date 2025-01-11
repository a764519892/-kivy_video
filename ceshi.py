from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
from kivy.uix.video import Video
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical')

        # Top spinner for selecting API source
        self.spinner = Spinner(size_hint=(1, None), height=50)
        self.spinner.bind(text=self.on_spinner_select)
        self.layout.add_widget(self.spinner)

        # Content area for displaying images
        self.scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=2, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        self.layout.add_widget(self.scroll_view)

        # Bottom buttons
        button_layout = BoxLayout(size_hint=(1, None), height=50)
        home_button = Button(text="MAIN")
        home_button.bind(on_release=lambda x: self.load_home())
        update_button = Button(text="UPDATE")
        update_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'update'))
        button_layout.add_widget(home_button)
        button_layout.add_widget(update_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

        # Initial data fetching
        self.page = 1
        self.api_url = None
        self.is_loading = False
        self.load_default_api()

    def load_default_api(self):
        default_api_url = "https://example.com/default-api"
        UrlRequest(default_api_url, self.populate_spinner, on_error=self.on_error, on_failure=self.on_error)

    def populate_spinner(self, request, result):
        self.spinner.values = [item['name'] for item in result]
        self.api_sources = {item['name']: item['api_url'] for item in result}
        if result:
            self.spinner.text = result[0]['name']

    def on_spinner_select(self, spinner, text):
        self.api_url = self.api_sources[text]
        self.page = 1
        self.grid_layout.clear_widgets()
        self.load_images()

    def load_images(self):
        if self.api_url and not self.is_loading:
            self.is_loading = True
            url = f"{self.api_url}?page={self.page}"
            UrlRequest(url, self.display_images, on_error=self.on_error, on_failure=self.on_error)

    def display_images(self, request, result):
        for item in result:
            img = AsyncImage(source=item['image_url'], size_hint_y=None, height=200)
            img.bind(on_touch_down=lambda instance, touch, video_url=item['video_url']: self.play_video(video_url) if instance.collide_point(*touch.pos) else None)
            self.grid_layout.add_widget(img)
        self.page += 1
        self.is_loading = False

    def load_home(self):
        self.grid_layout.clear_widgets()
        self.page = 1
        self.load_images()

    def on_error(self, request, error):
        self.is_loading = False
        print(f"Error loading data: {error}")

    def play_video(self, video_url):
        self.manager.get_screen('video').play(video_url)
        self.manager.current = 'video'

class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = Video(size_hint=(1, 1))
        self.add_widget(self.video)

        back_button = Button(text="Back", size_hint=(1, None), height=50)
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.add_widget(back_button)

    def play(self, video_url):
        Clock.schedule_once(lambda dt: self._play_video(video_url))

    def _play_video(self, video_url):
        self.video.source = video_url
        self.video.state = 'play'

class UpdateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="1.0.0", size_hint=(1, None), height=50))
        layout.add_widget(Label(text="[ref=log]REPEAD[/ref]", markup=True, size_hint=(1, None), height=50))
        back_button = Button(text="Back to Main", size_hint=(1, None), height=50)
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_button)
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(VideoScreen(name="video"))
        sm.add_widget(UpdateScreen(name="update"))
        return sm

if __name__ == "__main__":
    MyApp().run()
