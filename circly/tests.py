import datetime

from django import forms

from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext, loader
from django.test import TestCase, Client
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.views import generic

from models import Circle, Member, Invitation, Reminder

from choices_member import *
from forms import *

from helpers import clear_member_and_circle, set_member_and_circle, get_current_member, get_current_circle
from helpers import check_invite, check_owner, hash_code
from helpers import is_phone, is_email
from helpers import random_bitly

import phonenumbers

import bitly_api


def create_circle(first_name, circle_created_date=timezone.now()):
    Circle.objects.create(circle_name=first_name + "'s circle",
                          circle_created_date=circle_created_date)

def create_member(circle, member_name, circle_owner=False, member_created_date=timezone.now()):
    Member.objects.create(circle=circle,
                          circle_owner=circle_owner,
                          member_name=member_name,
                          member_created_date=member_created_date)

def create_invitation(member, invite_code, invite_short_url, invite_created_date=timezone.now()):
    Invitation.objects.create(member=next_member,
                              invite_code=invite_code, 
                              invite_short_url=new_short_url, 
                              invite_created_date=invite_created_date)

def create_reminder(member, reminder_subject, reminder_message, reminder_created_date=timezone.now(), reminder_send_date=timezone.now()):
    Reminder.objects.create(member=member,
                            reminder_subject=reminder_subject,
                            reminder_message=reminder_message,
                            reminder_created_date=reminder_created_date,
                            reminder_send_date=reminder_send_date)


class ModelTests(TestCase):
    def setUp(self):
        # Create two circles
        create_circle("Alice")
        create_circle("Bob")

        a_circle = Circle.objects.get(circle_name="Alice's circle")
        b_circle = Circle.objects.get(circle_name="Bob's circle")

        # Create eight members
        create_member(a_circle, "Alice", circle_owner=True)
        create_member(a_circle, "Chris")
        create_member(a_circle, "Dave")
        create_member(a_circle, "Esther")

        create_member(b_circle, "Bob", circle_owner=True)
        create_member(b_circle, "Frank")
        create_member(b_circle, "Gertrude")
        create_member(b_circle, "Heidi")

    def create_two_circles(self):
        a_circle = Circle.objects.get(circle_name="Alice's circle")
        b_circle = Circle.objects.get(circle_name="Bob's circle")

        a_member = Member.objects.get(member_name="Alice")
        c_member = Member.objects.get(member_name="Chris")
        d_member = Member.objects.get(member_name="Dave")
        e_member = Member.objects.get(member_name="Esther")

        b_member = Member.objects.get(member_name="Bob")
        f_member = Member.objects.get(member_name="Frank")
        g_member = Member.objects.get(member_name="Gertrude")
        h_member = Member.objects.get(member_name="Heidi")

        a_members = a_circle.member_set.all()
        b_members = b_circle.member_set.all()

        self.assertIn(a_member, a_members)
        self.assertIn(c_member, a_members)
        self.assertIn(d_member, a_members)
        self.assertIn(e_member, a_members)

        self.assertIn(b_member, b_members)
        self.assertIn(f_member, b_members)
        self.assertIn(g_member, b_members)
        self.assertIn(h_member, b_members)

        self.assertNotIn(a_member, b_members)
        self.assertNotIn(c_member, b_members)
        self.assertNotIn(d_member, b_members)
        self.assertNotIn(e_member, b_members)

        self.assertNotIn(b_member, a_members)
        self.assertNotIn(f_member, a_members)
        self.assertNotIn(g_member, a_members)
        self.assertNotIn(h_member, a_members)




#assertEqual(a, b)          a == b   
#assertNotEqual(a, b)       a != b   
#assertTrue(x)              bool(x) is True      
#assertFalse(x)             bool(x) is False     
#assertIs(a, b)             a is b
#assertIsNot(a, b)          a is not b
#assertIsNone(x)            x is None
#assertIsNotNone(x)         x is not None
#assertIn(a, b)             a in b
#assertNotIn(a, b)          a not in b
#assertIsInstance(a, b)     isinstance(a, b)
#assertNotIsInstance(a, b)  not isinstance(a, b)

#        self.assertEqual(lion.speak(), 'The lion says "roar"')
#        self.assertEqual(cat.speak(), 'The cat says "meow"')


# class QuestionViewTests(TestCase):
#     def test_index_view_with_no_questions(self):
#         """
#         If no questions exist, an appropriate message should be displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_index_view_with_a_past_question(self):
#         """
#         Questions with a pub_date in the past should be displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_index_view_with_a_future_question(self):
#         """
#         Questions with a pub_date in the future should not be displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.",
#                             status_code=200)
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_index_view_with_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         should be displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_index_view_with_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )


# class QuestionIndexDetailTests(TestCase):
#     def test_detail_view_with_a_future_question(self):
#         """
#         The detail view of a question with a pub_date in the future should
#         return a 404 not found.
#         """
#         future_question = create_question(question_text='Future question.',
#                                           days=5)
#         response = self.client.get(reverse('polls:detail',
#                                    args=(future_question.id,)))
#         self.assertEqual(response.status_code, 404)

#     def test_detail_view_with_a_past_question(self):
#         """
#         The detail view of a question with a pub_date in the past should
#         display the question's text.
#         """
#         past_question = create_question(question_text='Past Question.',
#                                         days=-5)
#         response = self.client.get(reverse('polls:detail',
#                                    args=(past_question.id,)))
#         self.assertContains(response, past_question.question_text,
#                             status_code=200)
