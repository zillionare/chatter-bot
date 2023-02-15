from sanic import response
from sanic.blueprints import Blueprint

bp = Blueprint('chatter', url_prefix='/chatter')

@bp.route("/status")
async def status(request):
    return response.text("OK")

@bp.route('/gpt3', method=["POST"])
async def gpt3(request):
    return response.text("OK")

@bp.route("/gpt35", method=["POST"])
async def gpt35(request):
    return response.text("OK")

