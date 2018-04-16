#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import base64
import os
import uuid

import pymysql
import tornado.concurrent
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

tornado.options.define("port", default=8000, type=int, help="port")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_secure_cookie('username', None)

        cur = self.application.conn.cursor()
        cur.callproc('select_XXX', ('car_brand',))
        car_brands = cur.fetchall()
        cur.callproc('select_XXX', ('car_type',))
        car_types = cur.fetchall()
        cur.callproc('select_XXX', ('car_age',))
        car_ages = cur.fetchall()
        cur.callproc('select_XXX', ('car_shift',))
        car_shifts = cur.fetchall()
        cur.callproc('select_XXX', ('car_color',))
        car_colors = cur.fetchall()
        cur.callproc('select_XXX', ('car_fuel',))
        car_fuels = cur.fetchall()

        cur.callproc('select_agent_info')
        agent_info = cur.fetchall()

        cur.callproc('select_car_info_random')
        car_info = cur.fetchall()

        cur.callproc('select_car_user_info_random')
        car_slider = cur.fetchall()

        cur.callproc('select_comment_random')
        comment_info = cur.fetchall()

        self.render('index.html', username=username, car_brands=car_brands, car_types=car_types, car_ages=car_ages,
                    car_shifts=car_shifts, car_colors=car_colors, car_fuels=car_fuels, agent_info=agent_info,
                    car_info=car_info, car_slider=car_slider, comment_info=comment_info)


class PropertyDetail(tornado.web.RequestHandler):
    def get(self):
        car_id = self.get_argument('id', None)
        if not car_id:
            self.write_error(404)
            return

        cur = self.application.conn.cursor()
        cur.callproc('select_car_detail_info', (car_id,))
        car_info = cur.fetchone()
        if not car_info:
            self.write_error(404)
            return

        cur.callproc('select_user_detail_info', (car_info[9],))
        user_info = cur.fetchone()

        cur.callproc('select_agent_detail_info', (car_info[10],))
        agent_info = cur.fetchone()

        my_info = [''] * 8

        if self.get_secure_cookie('username'):
            cur.callproc('select_user_detail_info', (self.get_secure_cookie('username').decode(),))
            my_info = cur.fetchone()

        self.render('Property-Details.html', user_info=user_info, car_info=car_info, agent_info=agent_info,
                    username=self.get_secure_cookie('username', None), my_info=my_info)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('Not-Found.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class PropertyListing(tornado.web.RequestHandler):
    def get(self):
        cur = self.application.conn.cursor()
        sql_select = 'SELECT car_name,car_door,car_seat,car_volume,car_saleprice,car_mileage,image_path,description,car_id FROM car_information WHERE on_sale=1 AND car_saleprice BETWEEN %d AND %d '
        price_min = 0
        price_max = 10000000
        for col in ['car_brand', 'car_type', 'car_age', 'car_shift', 'car_color', 'car_fuel', 'price-min', 'price-max']:
            value = self.get_argument(col, None)
            if value == '全部':
                continue
            if value:
                if col == 'price-min':
                    price_min = value
                elif col == 'price-max':
                    price_max = value
                else:
                    sql_select += ' AND ' + col + '=' + "'" + value + "'"
        try:
            cur.execute(sql_select % (int(price_min), int(price_max)))
        except Exception as e:
            self.write_error(500)
        else:
            car_info = cur.fetchall()
            self.render('Property-Listing.html', car_info=car_info, username=self.get_secure_cookie('username', None))

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class OurAgents(tornado.web.RequestHandler):
    def get(self):
        cur = self.application.conn.cursor()
        cur.callproc('select_four_agent')
        agent_info = cur.fetchall()
        self.render('About-Us.html', agent_info=agent_info, username=self.get_secure_cookie('username', None))


class Purchase(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        carid = self.get_argument('id', None)
        if carid:
            cur = self.application.conn.cursor()
            try:
                cur.callproc('select_account_price', (carid,))
                carinfo = cur.fetchone()
                if not carinfo:
                    self.write_error(404)
                    return
                if self.get_current_user() == carinfo[0].encode():
                    self.write_error(404)
                    return
                cur.callproc('update_account_price', (self.get_current_user().decode(), 0, carid))
                cur.callproc('insert_trade_detail', (carid, self.get_current_user().decode(), carinfo[1], carinfo[0]))
                self.application.conn.commit()
                self.application.newinfo.add(carinfo[0])
            except Exception as e:
                print(e)
                self.application.conn.rollback()
                return
            self.render('Purchased.html', username=self.get_secure_cookie('username', None))
        else:
            self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('Not-Found.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class applyChop(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        carid = self.get_argument('carid', None)
        chopid = self.get_argument('chopid', None)
        price = self.get_argument('price', None)
        username = self.get_argument('useraccount', None)
        if carid and chopid and price:
            cur = self.application.conn.cursor()
            try:
                cur.callproc('update_chop_saled', (chopid, carid))
                self.application.conn.commit()
                cur.callproc('update_car_price', (carid, price))
                self.application.conn.commit()
                cur.callproc('select_account_price', (carid,))
                carinfo = cur.fetchone()
                if not carinfo:
                    self.write_error(404)
                    self.application.conn.rollback()
                    return
                cur.callproc('update_account_price', (username, 0, carid))
                cur.callproc('insert_trade_detail', (carid, username, carinfo[1], carinfo[0]))
                self.application.conn.commit()
                self.application.newinfo.add(carinfo[0])
            except Exception as e:
                self.application.conn.rollback()
                return
            self.redirect('/TradeInfo')
        else:
            self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('Not-Found.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class rejectChop(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        chopid = self.get_argument('chopid', None)
        if chopid:
            try:
                cur = self.application.conn.cursor()
                cur.callproc('update_chop', (chopid, 2))
                self.application.conn.commit()
            except Exception as e:
                self.application.conn.rollback()
                self.write_error(404)
            else:
                self.redirect('/TradeInfo')
        else:
            self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('Not-Found.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class getChop(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def post(self):
        username = self.get_secure_cookie('username', None)
        formerowner = self.get_argument('formerowner', None)
        carid = self.get_argument('carid', None)
        price = self.get_argument('price', None)

        if username and formerowner and carid and price:
            try:
                cur = self.application.conn.cursor()
                cur.callproc('insert_chop', (username, formerowner, price, carid))
                self.application.conn.commit()
            except Exception as e:
                self.application.conn.rollback()
                self.write('fail')
            else:
                self.write('ok')


class Register(tornado.web.RequestHandler):
    def get(self):
        self.render('Register.html', username=self.get_secure_cookie('username', None))

    def post(self):
        USERNAME = self.get_argument('username', '')
        EMAIL = self.get_argument('email', '')
        PASSWORD = self.get_argument('password', '')
        if USERNAME.strip() == '' or PASSWORD.strip() == '' or EMAIL.strip() == '':
            self.write('failed')
        cur = self.application.conn.cursor()
        try:
            cur.callproc('insert_user_info', (USERNAME, EMAIL, PASSWORD))
            self.application.conn.commit()
            self.write('ok')
        except Exception as e:
            self.application.conn.rollback()
            self.write('failed')


class Login(tornado.web.RequestHandler):
    def post(self):
        USERNAME = self.get_argument('username', '')
        PASSWORD = self.get_argument('password', '')
        if USERNAME.strip() == '' or PASSWORD.strip() == '':
            self.write('failed')
        cur = self.application.conn.cursor()
        try:
            cur.callproc('select_user_password', (USERNAME,))
            pwd = cur.fetchone()
            if pwd and pwd[0] == PASSWORD:
                self.set_secure_cookie('username', USERNAME, expires_days=None)
                self.write('ok ' + USERNAME)
            else:
                self.write('failed')
        except Exception as e:
            raise e


class ContactUs(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    def get(self):
        self.render('Contact-Us.html', username=self.get_secure_cookie('username', None))

    @tornado.web.authenticated
    def post(self):
        cur = self.application.conn.cursor()
        try:
            cur.callproc('insert_comment', (
                self.get_secure_cookie('username'), self.get_argument('name'), self.get_argument('email'),
                self.get_argument('phone'), self.get_argument('title'), self.get_argument('message')))
            self.application.conn.commit()
            self.write('ok')
        except Exception as e:
            self.application.conn.rollback()
            self.write_error(500)

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class AboutUs(tornado.web.RequestHandler):
    def get(self):
        self.render('About-Us.html', username=self.get_secure_cookie('username', None))


class AdminLogin(tornado.web.RequestHandler):
    def get(self):
        self.render('Admin-Login.html')

    def post(self):
        if self.get_argument('adminname', None) and self.get_argument('password', None):
            cur = self.application.conn.cursor()
            cur.callproc('select_password', (self.get_argument('adminname'),))
            password = cur.fetchone()[0]
            if self.get_argument('password') == password:
                self.set_secure_cookie('adminname', self.get_argument('adminname'))
                self.write('ok')
            else:
                self.write('failed')


class NotFound(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('Not-Found.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class Logout(tornado.web.RequestHandler):
    def post(self):
        self.clear_all_cookies()
        self.write('ok')


class TradeInfo(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        cur = self.application.conn.cursor()
        cur.callproc('select_view_car_bought', (self.get_secure_cookie('username'),))
        car_bought = cur.fetchall()
        cur.callproc('select_view_car_sold1', (self.get_secure_cookie('username'),))
        car_sold1 = cur.fetchall()
        cur.callproc('select_view_car_sold0', (self.get_secure_cookie('username'),))
        car_sold0 = cur.fetchall()
        cur.callproc('select_chop', (self.get_secure_cookie('username'),))
        chop = cur.fetchall()
        cur.callproc('select_chopped', (self.get_secure_cookie('username'),))
        chopped = cur.fetchall()
        self.render('Trade-Info.html', username=self.get_secure_cookie('username', None), car_bought=car_bought,
                    car_sold=car_sold1 + car_sold0, chop=chop, chopped=chopped)


class UserInfo(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        cur = self.application.conn.cursor()
        cur.callproc('select_user_info_by_account', (self.get_current_user().decode(),))
        user_info = cur.fetchone()
        self.render('User-Info.html', username=self.get_current_user(), user_info=user_info)


class RemoveCar(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        if self.get_argument('id', None):
            cur = self.application.conn.cursor()
            cur.callproc('select_car_detail_info', (self.get_argument('id'),))
            res = cur.fetchone()
            owner = res[9]
            images = res[6]
            if owner == self.get_secure_cookie('username').decode():
                try:
                    cur.callproc('delete_car_info', (self.get_argument('id'),))
                    for image in images.split(';'):
                        if image:
                            os.remove(os.path.dirname(__file__) + image)
                    cur.callproc('update_count_agent')
                    self.application.conn.commit()
                    self.redirect('/TradeInfo')
                except Exception as e:
                    print(e)
                    self.application.conn.rollback()
                    self.write_error(500)
        else:
            self.write_error(500)

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class RemoveAgent(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie('adminname', None):
            self.redirect('/AdminLogin')
            return
        if self.get_argument('id', None):
            cur = self.application.conn.cursor()
            cur.callproc('select_agent_detail_info', (self.get_argument('id'),))
            res = cur.fetchone()
            image = res[5]
            try:
                cur.callproc('delete_agent', (self.get_argument('id'),))
                if image:
                    os.remove(os.path.dirname(__file__) + image)
                cur.callproc('update_count_agent')
                self.application.conn.commit()
                self.redirect('/Manage')
            except Exception as e:
                print(e)
                self.application.conn.rollback()
                self.write_error(500)
        else:
            self.write_error(500)

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class RemoveUser(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie('adminname', None):
            self.redirect('/AdminLogin')
            return
        if self.get_argument('id', None):
            cur = self.application.conn.cursor()
            cur.callproc('select_user_detail_info', (self.get_argument('id'),))
            res = cur.fetchone()
            image = res[5]
            try:
                cur.callproc('delete_user', (self.get_argument('id'),))
                if image and image!='/static/image/user-default.jpg':
                    os.remove(os.path.dirname(__file__) + image)
                cur.callproc('update_count_agent')
                self.application.conn.commit()
                self.redirect('/Manage')
            except Exception as e:
                print(e)
                self.application.conn.rollback()
                self.write_error(500)
        else:
            self.write_error(500)

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class RemoveCarAdmin(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie('adminname', None):
            self.redirect('/AdminLogin')
            return
        if self.get_argument('id', None):
            cur = self.application.conn.cursor()
            cur.callproc('select_car_detail_info', (self.get_argument('id'),))
            res = cur.fetchone()
            images = res[6]
            try:
                cur.callproc('delete_car_info', (self.get_argument('id'),))
                for image in images.split(';'):
                    if image:
                        os.remove(os.path.dirname(__file__) + image)
                cur.callproc('update_count_agent')
                self.application.conn.commit()
                self.redirect('/Manage')
            except Exception as e:
                print(e)
                self.application.conn.rollback()
                self.write_error(500)
        else:
            self.write_error(500)

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class RemoveComment(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie('adminname', None):
            self.redirect('/AdminLogin')
            return
        if self.get_argument('id', None):
            cur = self.application.conn.cursor()
            try:
                cur.callproc('delete_comment', (self.get_argument('id'),))
                self.application.conn.commit()
                self.redirect('/Manage')
            except Exception as e:
                print(e)
                self.application.conn.rollback()
                self.write_error(500)
        else:
            self.write_error(500)

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.render('Server-Error.html', username=self.get_secure_cookie('username', None))
        else:
            self.write('error:' + str(status_code))


class Manage(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie('adminname', None):
            cur = self.application.conn.cursor()
            cur.callproc('select_count_user')
            users = cur.fetchone()[0]
            cur.callproc('select_count_agent')
            agents = cur.fetchone()[0]
            cur.callproc('select_count_car_information')
            cars = cur.fetchone()[0]
            cur.callproc('select_count_trade_detail')
            trades = cur.fetchone()[0]
            cur.callproc('select_count_comment')
            comments = cur.fetchone()[0]
            cur.callproc('select_agent_sale_info_current_month')
            saleinfo1 = cur.fetchall()
            cur.callproc('select_agent_sale_info')
            saleinfo2 = cur.fetchall()
            cur.callproc('manage_user')
            manage_user = cur.fetchall()
            cur.callproc('manage_car')
            manage_car = cur.fetchall()
            cur.callproc('manage_comment')
            manage_comment = cur.fetchall()

            self.render('Manage.html', username=self.get_secure_cookie('adminname', None), users=users, agents=agents,
                        cars=cars, trades=trades, comments=comments,
                        sale_info=[s[0] + s[1] for s in zip(saleinfo1, saleinfo2)], manage_user=manage_user,
                        manage_car=manage_car, manage_comment=manage_comment)
        else:
            self.redirect('/AdminLogin')

    def post(self):
        if not self.get_secure_cookie('adminname', None):
            self.write_error(403)
            return

        cur = self.application.conn.cursor()
        try:
            cur.callproc('insert_agent_info', (
                self.get_argument('agent_name'), self.get_argument('agent_phone'), self.get_argument('agent_email'),
                self.get_argument('agent_position'), self.get_argument('agent_url')))
            self.application.conn.commit()
            agentid = cur.fetchone()[0]
        except Exception as e:
            self.application.conn.rollback()
            self.write('failed')
            return

        img_path = ''

        file_metas = self.request.files['files']
        if len(file_metas):
            meta = file_metas[0]
            filename = meta['filename']
            img_name = 'agent-' + str(agentid) + os.path.splitext(filename)[1]
            img_path += os.path.join('/', 'static', 'image', img_name)
            try:
                with open(os.path.join(os.path.dirname(__file__), 'static', 'image', img_name), 'wb') as f:
                    f.write(meta['body'])
                cur.callproc('update_agent_photo', (agentid, img_path))
                self.application.conn.commit()
            except Exception as e:
                self.write('failed')
                return
            self.write('ok')

        else:
            self.write('failed')


class PollingHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        self.application.newinfo.remove(self.get_secure_cookie('username').decode())

    @tornado.web.authenticated
    def post(self):
        if self.get_secure_cookie('username').decode() in self.application.newinfo:
            self.write('ok')
        else:
            self.write('no')


class MapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('map.html')


class UpdateUserImg(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def post(self):
        file_metas = self.request.files['files']
        if len(file_metas):
            filename = file_metas[0]['filename']
            img_name = self.get_current_user().decode() + '-img' + os.path.splitext(filename)[1]
            try:
                with open(os.path.join(os.path.dirname(__file__), 'static', 'image', img_name), 'wb') as f:
                    f.write(file_metas[0]['body'])
            except Exception as e:
                self.write('fail')
                return

            else:
                cur = self.application.conn.cursor()
                try:
                    cur.callproc('update_user_img',
                                 (os.path.join('/', 'static', 'image', img_name), self.get_current_user().decode()))
                    self.application.conn.commit()
                    self.write('ok')
                except Exception as e:
                    self.application.conn.rollback()
                    self.write('fail')
                    return
        self.write('fail')


class UpdateUserInfo(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def post(self):
        for col in ['user_name', 'user_idnumber', 'user_birthday', 'user_gender', 'user_nationality',
                    'user_email', 'user_phone']:
            data = self.get_argument(col, None)
            if data:
                cur = self.application.conn.cursor()
                try:
                    cur.callproc('set_user_info', (col, data, self.get_current_user().decode()))
                    self.application.conn.commit()
                except Exception as e:
                    print(e)
                    self.application.conn.rollback()
                    self.write('fail')
                    return

        cur = self.application.conn.cursor()
        cur.callproc('update_user_password',
                     (self.get_current_user().decode(), self.get_argument('user_password', None)))
        self.application.conn.commit()
        self.redirect('/UserInfo')


class NewCar(tornado.web.RequestHandler):
    def get_current_user(self):
        loggedin = self.get_secure_cookie('username', None)
        return loggedin

    @tornado.web.authenticated
    def get(self):
        cur = self.application.conn.cursor()
        cur.callproc('select_agent_name')
        agent_info = cur.fetchall()
        self.render('Car-Info.html', username=self.get_current_user().decode(), agent_info=agent_info)

    @tornado.web.authenticated
    def post(self):
        cur = self.application.conn.cursor()
        cur.callproc('select_agent_info_by_name', (self.get_argument('agent_name'),))
        agentid = cur.fetchone()[0]
        cur = self.application.conn.cursor()
        carid = 0
        try:
            cur.callproc('insert_car_info', (
                self.get_argument('car_name'), self.get_argument('car_price'), self.get_argument('car_brand'),
                self.get_argument('car_type'), self.get_argument('car_mileage'), self.get_argument('car_door'),
                self.get_argument('car_seat'), self.get_argument('car_volume'), self.get_argument('car_shift'),
                self.get_argument('car_color'), self.get_argument('car_saleprice'), agentid,
                self.get_argument('note'), self.get_current_user().decode(), self.get_argument('description'),
                self.get_argument('car_age'), self.get_argument('car_fuel')))
            self.application.conn.commit()
            carid = cur.fetchone()[0]
        except Exception as e:
            self.application.conn.rollback()
            return

        img_path = ''

        file_metas = self.request.files['files']
        if len(file_metas):
            for meta in enumerate(file_metas, start=1):
                filename = meta[1]['filename']
                img_name = 'car-' + str(carid) + '-' + str(meta[0]) + os.path.splitext(filename)[1]
                img_path += os.path.join('/', 'static', 'image', img_name) + ';'
                try:
                    with open(os.path.join(os.path.dirname(__file__), 'static', 'image', img_name), 'wb') as f:
                        f.write(meta[1]['body'])
                except Exception as e:
                    print(e)
                    self.write('fail')
                    return

            cur = self.application.conn.cursor()
            try:
                cur.callproc('update_car_img',
                             (img_path, carid))
                self.application.conn.commit()
                self.redirect('/PropertyDetail?id=' + str(carid))
                return
            except Exception as e:
                print(e)
                self.application.conn.rollback()
                self.write('fail')
                return
        self.write('fail')


class Application(tornado.web.Application):
    def __init__(self):
        cookie_sec = base64.b64encode(uuid.uuid4().bytes)
        handlers = [
            (r'/index', tornado.web.RedirectHandler, {'url': '/'}),
            (r'/', IndexHandler),
            (r'/PropertyDetail', PropertyDetail),
            (r'/PropertyListing', PropertyListing),
            (r'/OurAgents', OurAgents),
            (r'/Register', Register),
            (r'/ContactUs', ContactUs),
            (r'/AboutUs', AboutUs),
            (r'/Login', Login),
            (r'/Logout', Logout),
            (r'/Purchase', Purchase),
            (r'/UserInfo', UserInfo),
            (r'/UpdateUesrImg', UpdateUserImg),
            (r'/UpdateUserInfo', UpdateUserInfo),
            (r'/NewCar', NewCar),
            (r'/TradeInfo', TradeInfo),
            (r'/Manage', Manage),
            (r'/Polling', PollingHandler),
            (r'/AdminLogin', AdminLogin),
            (r'/RemoveCar', RemoveCar),
            (r'/ApplyChop', applyChop),
            (r'/RejectChop', rejectChop),
            (r'/GetChop', getChop),
            (r'/Map', MapHandler),
            (r'/RemoveCarAdmin', RemoveCarAdmin),
            (r'/RemoveAgent', RemoveAgent),
            (r'/RemoveUser', RemoveUser),
            (r'/RemoveComment', RemoveComment),
            (r'.*', NotFound)
        ]

        settings = dict(static_path=os.path.join(
            os.path.dirname(__file__), 'static'), template_path=os.path.join(
            os.path.dirname(__file__), 'template'), debug=True,
            cookie_secret=cookie_sec, xsrf_cookies=True, login_url="/Register")

        super().__init__(handlers, **settings)

        self.conn = pymysql.connect(host="127.0.0.1", user="root",
                                    password="Aa111111", db="real_estate", port=3306, charset='utf8mb4')

        self.newinfo = set()


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
