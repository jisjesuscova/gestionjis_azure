from flask import Blueprint, render_template, request, redirect, url_for
from app.employee_labor_data.employee_labor_datum import EmployeeLaborDatum
from flask import jsonify, make_response
from app.helpers.helper import Helper
from app.employees_turns.employee_turn import EmployeeTurn
from app.turns.turn import Turn
import json


turn = Blueprint("turns", __name__)

@turn.before_request
def constructor():
   pass

@turn.route("/turns/types/<rut>/<group_id>", methods=['GET'])
def index(rut, group_id):
   employee_labor_datum = EmployeeLaborDatum.get(rut)
   id = employee_labor_datum.employee_type_id

   turns = Turn.get_by_employee_type_group(id, group_id)
   turns = Helper.serialize(turns, 2)
   
   return json.dumps(turns)


@turn.route("/turns/pre_store", methods=['POST'])
def pre_store():
   status = EmployeeTurn.pre_store(request.form)

   return json.dumps(status)


@turn.route("/turns/free_days/<id>", methods=['GET'])
@turn.route("/turns/free_days", methods=['GET'])
def free_day(id):
   turn = Turn.get_special(id)
   days = Helper.serialize(turn, 3)

   return json.dumps(days)

@turn.route("/turns/calculate/<id>", methods=['GET'])
@turn.route("/turns/calculate", methods=['GET'])
def calculate(id):
   turn = Turn.get(id)
   seconds = Helper.get_seconds(turn)
   hours = Helper.get_total_hour_weeks(seconds, turn.group_day_id)

   return str(hours)