import sys
import os
import boto3
import logging
import urllib.parse
from airflow.models import Variable
from airflow.utils.email import send_email
from airflow.models.xcom import XCom
import NotificationConstants
from datetime import datetime


class CommonUtils:
    def send_email_alert(ti,context):
        try:
            task_instance = context['task_instance']
            email_str = context['params'].get('email_list')
            to_email = email_str.split(",")
            dag_name = context['dag'].dag_id
            dag_run_id = context['run_id']
            dag_run_id_url = dag_run_id.replace(":", "_")
            task_id = context['task'].task_id
            execution_date = context['execution_date']
            task_output = XCom.get_one(key=task_id, execution_date=execution_date)
            task_status = task_output['status']
            # task_status = ti.xcom_pull(key=task_id)['status']
            
            subject = f"Airflow {dag_name}: {task_status}"
            logging.info(f"Sending email alert for {dag_name} with subject {subject}")
            logging.info(f"Task status is {task_status}")
            logging.info(f"Task instance log url is {task_instance.log_url}")
            if task_status in ["SUCCESS","RUNNING"]:
                logging.info(f"Task status is {task_status}")
                logging.info("Started creating HTML content for SUCCESS")
                html_content = NotificationConstants.SUCCESS_NOTIFICATION_HTML_FILE
                html_content = html_content.replace("$$dag_name$$",dag_name)
                html_content = html_content.replace("$$dag_id$$",dag_name)
                html_content = html_content.replace("$$run_id$$",dag_run_id)
                html_content = html_content.replace("$$status$$",task_status)
                html_content = html_content.replace("$$execution_date$$",str(context['execution_date']))
                html_content = html_content.replace("$$pipeline_url$$",f"{task_instance.log_url}")
                logging.info(f"HTML content for SUCCESS is created")
            elif task_status in ["FAILED","ERROR"]:
                error_msg = task_output['error']
                logging.info(f"Task status is {task_status}")
                logging.info("Started creating HTML content for FAILED")
                html_content = NotificationConstants.ERROR_NOTIFICATION_HTML_FILE
                html_content = html_content.replace("$$dag_name$$",dag_name)
                html_content = html_content.replace("$$dag_id$$",dag_name)
                html_content = html_content.replace("$$run_id$$",dag_run_id)
                html_content = html_content.replace("$$status$$",task_status)
                html_content = html_content.replace("$$execution_date$$",str(context['execution_date']))
                html_content = html_content.replace("$$pipeline_url$$",f"{task_instance.log_url}")
                html_content = html_content.replace("$$error_message$$",error_msg)
                logging.info("Started Creating URL for log stream")
                log_group_name = Variable.get("AIRFLOW_TASK_LOG_GROUP_NAME")
                log_stream_name_prefix = f"dag_id={dag_name}/run_id={dag_run_id_url}/task_id={task_id}/attempt=1.log"
                region = 'us-east-1'  # Replace with your AWS region
                base_url = f'https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#logsV2:log-groups/log-group/{log_group_name}'
                log_stream_name_prefix = urllib.parse.quote(log_stream_name_prefix, safe='')
                log_stream_param = f'log-events/{log_stream_name_prefix}'
                final_url = f'{base_url}/{log_stream_param}'
                logging.info("URL for log stream is created")
                logging.info(f"Final URL is {final_url}")
                html_content = html_content.replace("$$log_url$$",final_url)
                logging.info(f"HTML content for FAILED is created")
                
            logging.info(f"Sending email alert for {dag_name} with subject {subject}")
            send_email(to=to_email, subject=subject, html_content=html_content)
            logging.info(f"Email alert for {dag_name} with subject {subject} is sent")
            
        except Exception as e:
            print(f"Failed to describe log streams: {e}")
            raise e