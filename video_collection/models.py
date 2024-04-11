from django.db import models
from django.core.exceptions import ValidationError
from urllib import parse


class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        try:
            url_components = parse.urlparse(self.url) # feed it to parsing libary

            # check if the url matches youtube's url formatting or deny it.
            if url_components.scheme != "https" or url_components.netloc != "www.youtube.com" or url_components.path != '/watch':
                raise ValidationError(f'Invalid Youtube URL {self.url}')

            query_string = url_components.query

            if not query_string: # No query string? Bad URL.
                raise ValidationError(f'Invalid Youtube URL {self.url}')

            parameters = parse.parse_qs(query_string, strict_parsing=True)
            parameters_list = parameters.get('v')

            if not parameters_list: # No parameters? No good youtube IDs.
                raise ValidationError(f'Invalid Youtube parameters {self.url}')

            self.video_id = parameters_list[0]

        except ValueError as e:
            raise ValidationError(f'Unable to parse URL {self.url}') from e

        super().save(*args, **kwargs)


    def __str__(self):

        if not self.notes:
            self.notes = "No Notes."

        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Notes: {self.notes[:200]}'
