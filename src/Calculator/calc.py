import json
import re
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

HISTORY_SIZE = 30
STATUSES = ["success", "fail"]
OPERATIONS = ["+", "-", "*", "/"]

app = FastAPI()


class Expression(BaseModel):
    expr: str


def updateHistory(response):
    try:
        with open("calcHistory.json", "r") as jsonFile:
            hist = json.load(jsonFile)
        if len(hist) <= HISTORY_SIZE - 1:
            hist[len(hist)] = response
        else:
            for i in range(1, HISTORY_SIZE):
                hist[str(i - 1)] = hist[str(i)]
            hist[str(HISTORY_SIZE - 1)] = response
        with open("calcHistory.json", "w") as jsonFile:
            json.dump(hist, jsonFile, indent=2)
    except FileNotFoundError:
        with open("calcHistory.json", "w") as jsonFile:
            data = {0: response}
            json.dump(data, jsonFile, indent=2)


def getHistory(limit, status):
    try:
        with open("calcHistory.json", "r") as jsonFile:
            hist = json.load(jsonFile)
        response = []
        historySize = len(hist)
        if status and status not in STATUSES:
            raise HTTPException(status_code=400, detail="Error: Wrong input. Status must be 'success' or 'fail'.")
        elif limit > HISTORY_SIZE or limit < 1:
            raise HTTPException(status_code=400, detail="Error: Wrong input. Limit must be in range 1 - 30.")
        if status:
            response.append([hist[str(i)] for i in range(historySize-1, -1, -1)
                             if hist[str(i)]["status"] == status])
            if limit < historySize:
                response[0] = response[0][:limit]
            return response[0]
        if limit < historySize:
            response.append([hist[str(i)] for i in range(historySize - 1, historySize - limit - 1, -1)])
        else:
            response.append([hist[str(i)] for i in range(historySize - 1, -1, -1)])
        return response[0]
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Error: No history")


@app.get("/history")
def history(limit: int = 30, status: str = None):
    return getHistory(limit, status)


def opCalc(op, first, second):
    if op == "+":
        return first + second
    elif op == "-":
        return first - second
    elif op == "*":
        return first * second
    elif op == "/":
        return first / second


def calculate(expr):
    for_check = expr.replace(" ", "")
    for_check_len = len(for_check)
    newExpr = ""
    answer = ""
    first = True
    if re.match(r"^([+\-]?(\d*\.)?\d*)$", for_check):
        answer = float(re.match(r"^([+\-]?(\d*\.)?\d*)$", for_check).group())
    else:
        while len(newExpr) < for_check_len:
            example = re.match(r"([+\-]?(\d*\.)?\d*)([+\-*/])(-?(\d*\.)?\d*)", for_check)
            if example:
                if first:
                    newExpr += example.group(1)
                    first = False
                newExpr += example.group(3) + example.group(4)
                try:
                    arg1 = float(example.group(1))
                    arg2 = float(example.group(4))
                    op = example.group(3)
                except ValueError:
                    answer = ""
                    break
                if op not in OPERATIONS:
                    answer = ""
                    break
                if op == "/" and arg2 == 0:
                    answer = ""
                    break
                answer = opCalc(op, arg1, arg2)
                for_check = str(answer) + for_check[len(newExpr):]
            else:
                answer = ""
                break
    return answer


def getAnswer(expr):
    answer = calculate(expr)
    if answer != "":
        response = {"request": expr, "response": round(answer, 3), "status": "success"}
        updateHistory(response)
        return round(answer, 3)
    else:
        response = {"request": expr, "response": answer, "status": "fail"}
        updateHistory(response)
        raise HTTPException(status_code=400, detail="Arithmetic expression entered incorrectly")


@app.post("/calc")
def calc(expression: Expression):
    return getAnswer(expression.expr)


if __name__ == '__main__':
    uvicorn.run(
        "calc:app",
        host='localhost',
        port=8080,
        reload=True
    )
