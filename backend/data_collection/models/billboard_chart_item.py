class BillboardChartItem:
    def __init__(self, artist, song, rank, last_week, two_weeks_ago, peak_position, weeks_on_chart, riaa, song_writers, producers, imprint_promotion_label):
        self.artist = artist
        self.song = song
        self.rank = rank
        self.last_week = last_week
        self.two_weeks_ago = two_weeks_ago
        self.peak_position = peak_position
        self.weeks_on_chart = weeks_on_chart
        self.riaa = riaa
        self.song_writers = song_writers
        self.producers = producers
        self.imprint_promotion_label = imprint_promotion_label

    def serialize(self):
        return {
            "artist": self.artist,
            "song": self.song,
            "rank": self.rank,
            "last_week": self.last_week,
            "two_weeks_ago": self.two_weeks_ago,
            "peak_position": self.peak_position,
            "weeks_on_chart": self.weeks_on_chart,
            "riaa": self.riaa,
            "song_writers": self.song_writers,
            "producers": self.producers,
            "imprint_promotion_label": self.imprint_promotion_label
        }
        