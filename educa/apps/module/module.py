class ModuleObject:
    def __init__(self, id_, title, order, lessons=None, video_duration=0):
        if lessons is None:
            lessons = []
        self.id = id_
        self.title = title
        self.lessons = lessons
        self.order = order
        self.video_duration = video_duration

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def __repr__(self):
        return f'{self.title} - {self.lessons}'


class LessonObject:
    def __init__(self, id_, title, order, video_duration):
        self.id = id_
        self.title = title
        self.order = order
        self.video_duration = video_duration

    def __repr__(self):
        return f'{self.title}'
