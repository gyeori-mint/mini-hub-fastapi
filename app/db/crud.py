from app.db.models import *


def read_projects(session, status=True):
    rows = session.query(TbProjectInfo).filter_by(status=status).all()
    return rows


def read_user_id_by_slack_id(session, slack_id):
    row = session.query(TbManagerInfo).filter_by(slack_id=slack_id).first()
    return row.id


def create_project(session, project_dict):
    project_record = TbProjectInfo(name=project_dict['name'],
                                   company_name=project_dict['company_name'],
                                   main_manager_id=project_dict['main_manager_id'],
                                   sub_manager_id=project_dict['sub_manager_id'])
    session.add(project_record)
    session.commit()


def update_budgets(session, budget_dict):
    budget_record = TbMonthlyBudget(year=budget_dict['year'],
                                    month=budget_dict['month'],
                                    project_id=budget_dict['project_id'],
                                    budget=budget_dict['budget'])
    session.add(budget_record)
    session.commit()


def update_adjustment(session, adjustment_dict):
    adjustment_record = TbMonthlyAdjusted(year=adjustment_dict['year'],
                                      month=adjustment_dict['month'],
                                      project_id=adjustment_dict['project_id'],
                                      adjusted_spend=adjustment_dict['adjusted_spend'])
    session.add(adjustment_recordt)
    session.commit()
