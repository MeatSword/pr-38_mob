import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from dino import dino_questions

class DinoQuizApp(App):
    def build(self):
        self.score = 0
        self.current_question = 0
        self.questions = random.sample(dino_questions, len(dino_questions))
        
        self.layout = BoxLayout(orientation='vertical')
        
        self.image = Image()
        self.layout.add_widget(self.image)
        
        self.question_label = Label(font_size='20sp')
        self.layout.add_widget(self.question_label)
        
        self.answer_input = TextInput(multiline=False, size_hint_y=None, height='40dp')
        self.layout.add_widget(self.answer_input)
        
        self.submit_button = Button(text='Ответить', size_hint_y=None, height='48dp')
        self.submit_button.bind(on_press=self.check_answer)
        self.layout.add_widget(self.submit_button)
        
        self.result_label = Label(font_size='20sp')
        self.layout.add_widget(self.result_label)
        
        self.update_question()
        
        # Load sounds
        self.correct_sound = SoundLoader.load('sounds/correct.mp3')
        self.wrong_sound = SoundLoader.load('sounds/wrong.mp3')
        self.background_music = SoundLoader.load('sounds/background.mp3')
        self.background_music.loop = True
        self.background_music.play()
        
        return self.layout

    def update_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.image.source = question['image']
            self.question_label.text = question['question']
            self.answer_input.text = ''
            self.result_label.text = ''
        else:
            self.show_results()

    def check_answer(self, instance):
        answer = self.answer_input.text.strip().lower()
        correct_answer = self.questions[self.current_question]['answer'].strip().lower()
        
        if answer == correct_answer:
            self.score += 1
            self.result_label.text = 'Правильно!'
            if self.correct_sound:
                self.correct_sound.play()
        else:
            self.result_label.text = f'Неправильно! Правильный ответ: {self.questions[self.current_question]["answer"]}'
            if self.wrong_sound:
                self.wrong_sound.play()
        
        self.current_question += 1
        Clock.schedule_once(lambda dt: self.update_question(), 2)

    def show_results(self):
        content = BoxLayout(orientation='vertical')
        result_label = Label(text=f'Ваш результат: {self.score} из {len(self.questions)}')
        content.add_widget(result_label)
        
        close_button = Button(text='Закрыть')
        content.add_widget(close_button)
        
        popup = Popup(title='Результаты', content=content, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    DinoQuizApp().run()