# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, List, Optional, Sequence, Union

# from airflow.hooks.sqlite_hook import SqliteHook
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.email import send_email

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pandas as pd
# import pandas.io.sql as psql


# from sqlalchemy.inspection import inspect
# from sqlalchemy.engine.reflection import Inspector
# from airflow.models.serialized_dag import SerializedDagModel
# import os


class EmailFromDbOperator(BaseOperator):
    """
    Sends an email.

    :param to: list of emails to send the email to. (templated)
    :param subject: subject line for the email. (templated)
    :param html_content: content of the email, html markup
        is allowed. (templated)
    :param files: file names to attach in email (templated)
    :param cc: list of recipients to be added in CC field
    :param bcc: list of recipients to be added in BCC field
    :param mime_subtype: MIME sub content type
    :param mime_charset: character set parameter added to the Content-Type
        header.
    :param custom_headers: additional headers to add to the MIME message.
    """


    ui_color = '#e6faf9'

    def __init__(
        self,
        db_conn_id='mssql_default',
        database=None,
        conn_id: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.db_conn_id = db_conn_id
        self.database = database
        self.conn_id = conn_id
        # self.custom_headers = custom_headers



    def execute(self, context: Context):
        import re

        print('EmailFromDbOperator:test!!')
        # send_email(
        #     self.to,
        #     self.subject,
        #     self.html_content,
        #     files=self.files,
        #     cc=self.cc,
        #     bcc=self.bcc,
        #     mime_subtype=self.mime_subtype,
        #     mime_charset=self.mime_charset,
        #     conn_id=self.conn_id,
        #     custom_headers=self.custom_headers,
        # )
        
        # retrieving your SQL Alchemy connection
        # if you are using Astro CLI this env variable will be set up automatically
        df = self.get_mail_property()
        print('BEFORE SEND MAIL >>>>')
        # Handle if NONE, if Error
        for index, row in df.iterrows():
            # print(
            #     row['to'],
            #     row['subject'],
            #     row['html_content'],
            #     # conn_id=self.conn_id,
            # )
            to_list = re.split('; |, |\n',row['to'])
            send_email(
                to_list,
                row['subject'],
                row['html_content'],
                # conn_id=self.conn_id,
            )
            # Update process status, P: process, F: Fail, S: Success


    def get_mail_property(self):
        # postgres_hook = PostgresHook(postgres_conn_id="airflow_db")
        # sql_alchemy_conn
        # hook = SqliteHook(sqlite_conn_id="airflow_db")
        # print('db mail test:::>')
        # print(hook.get_conn())
        # print(hook.get_uri())
 
        mysql = """
            select dag_id, is_paused, next_dagrun_data_interval_end  from dag
        # """        
        # engine = hook.get_sqlalchemy_engine()
        # df = hook.get_pandas_df(mysql)


        # print(df)
        # print('db mail test <<<<')
        # TODO: to a list 
        df = pd.DataFrame({
            'to':['web.jesse@gmail.com,iec.jesse@gmail.com','jessewei_tw@hotmail.com'], 
            'subject':['<ODP:ALERT:QAM>','<ODP:ALERT:PRO>' ], 
            'html_content':['Mail test in html#1', 'Mail test in html#2'], 
            })
        return df
