from django.contrib import admin

from newsletter.models import Subscriber



@admin.register(Subscriber)
class SubscriberAdminConfig(admin.ModelAdmin):
    model = Subscriber

# CREATE TABLE "newsletter_subscriber" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(255) NULL UNIQUE, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL)