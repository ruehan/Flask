from datetime import datetime, timedelta
import math

from flask.json import jsonify

def cvtDt2Str(dt, isMs=False):
    assert isinstance(dt, datetime)
    if isMs:
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")

def cvtTimestamp2Str(timestamp, isMs=False):
    assert isinstance(timestamp, int) or isinstance(timestamp, float)
    dt = datetime.fromtimestamp(timestamp)
    return cvtDt2Str(dt, isMs)



def getResDict(pageIndex, pageOffset, pageSize, resultData, rowCnt, sortingType):
    if 0 == pageSize:
        pageSize = len(resultData)
    addLastPage = 0 if rowCnt % pageSize == 0 else 1
    return {
        "result" : "pulled",
        "result_msg" : f"data rows: {len(resultData)}",
        "data" : resultData,
        "pageInfo": {
            "lastPage" : rowCnt // pageSize + addLastPage,
            "page" : pageIndex +1,
            "offset": pageOffset,
            "pageSize": pageSize,
            "dataCnt" : rowCnt,
            "sortingType" : sortingType
        }
    }

class PageNav:
    @staticmethod
    def getPageInfo(page, pageSize, dataCount, pageNavSize = 7):
        """
        """
        dataLastPage = math.ceil(dataCount / pageSize) + 1
        firstPage = page - math.floor(pageNavSize / 2)
        if firstPage <= 0:
            firstPage = 1
        lastPage = firstPage + pageNavSize
        if lastPage > dataLastPage:
            lastPage = dataLastPage
            firstPage = lastPage - pageNavSize
            if firstPage <= 0:
                firstPage = 1
        return {
            "page": page,
            "pages": list(range(firstPage, lastPage)),
            "pageSize": pageSize,
            "dataCount": dataCount,
            "lastPage": dataLastPage - 1
        }

def getKeyVal(dictKey, dictObj):
    """
    return value or None
    """
    if isinstance(dictObj, dict) and dictKey in dictObj.keys():
        return dictObj[dictKey]
    return None

def hasKeys(needKeys, receiveKeys):
    """
    return bool(has), str(message) or None
    """
    for itNeedKey in needKeys:
        if itNeedKey not in receiveKeys:
            return False, f"Not has key '{itNeedKey}' in received data keys"
    return True, None

def getJsonMsg(msg):
    """
    msg: string
    return jsonify({"msg": msg})
    """
    return jsonify({"msg":msg})

# ===== get data db =====
def getDataDb(dbModel, reqDataDict, pageInfoDict):
    """일반적인 데이터 조회 함수"""
    # todo 예외처리가 필요한 과정이 있는지 검토 할 것
    # assert isinstance(dbModel, db.Model)
    rowCnt, rows, pageSize, pageIndex, pageOffset = -1, None, 0, -1, -1
    sensorId = reqDataDict["dev_id"]
    datetimeRange = reqDataDict["range"]
    # print("getdataDb()","reqDataDict:", reqDataDict)
    # print("getdataDb()","pageInfoDict:", pageInfoDict)
    # todo datetimeRange 가 None 인경우 응답을 고민할 것
    if len(datetimeRange) > 0:
        dt1 = datetime.fromtimestamp(datetimeRange[0])
        dt1Str = dt1.strftime("%Y-%m-%d %H:%M:%S")
        pageSize = pageInfoDict["pageSize"]
        pageIndex = pageInfoDict["page"] -1
        sortingType = pageInfoDict["sortingType"]
        if pageIndex < 0 and "offset" in pageInfoDict:
            # offet 이 있는 경우
            pageOffset = pageInfoDict["offset"]
            if pageSize > 0:
                # data count 로 요청한 경우
                rowCnt = pageSize
                rows = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str) 
                    ).limit(pageSize).offset(pageOffset).all()
            else:
                # data date range 로 요청한 경우
                dt2 = datetime.fromtimestamp(datetimeRange[1]) + timedelta(days=1)
                dt2Str = dt2.strftime("%Y-%m-%d %H:%M:%S")
                # 
                tmpQuery = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str) & (dbModel.datetimes <= dt2Str) 
                    ).offset(pageOffset)
                rowCnt = tmpQuery.count()
                rows = tmpQuery.all()
        else:
            # 일반적인 page 기반 조회 == offset이 없는 경우
            if 1 == len(datetimeRange):
                # print("sensorId:", sensorId, ", dt1Str:", dt1Str)
                rowCnt = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str) ).count()
                if "Descending" == sortingType:
                    rows = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str)
                        ).order_by(dbModel.datetimes.desc() ).limit(pageSize).offset(pageIndex * pageSize).all()
                else:
                    rows = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str)
                        ).order_by(dbModel.datetimes.asc() ).limit(pageSize).offset(pageIndex * pageSize).all()
            elif 2 == len(datetimeRange):
                dt2 = datetime.fromtimestamp(datetimeRange[1]) + timedelta(days=1)
                dt2Str = dt2.strftime("%Y-%m-%d %H:%M:%S")
                rowCnt = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str) & (dbModel.datetimes <= dt2Str) ).count()
                if "Descending" == sortingType:
                    rows = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str) & (dbModel.datetimes <= dt2Str) 
                        ).order_by(dbModel.datetimes.desc() ).limit(pageSize).offset(pageIndex * pageSize).all()
                else:
                    rows = dbModel.query.filter( (dbModel.dev_id == sensorId) & (dbModel.datetimes >= dt1Str) & (dbModel.datetimes <= dt2Str) 
                        ).order_by(dbModel.datetimes.asc() ).limit(pageSize).offset(pageIndex * pageSize).all()
    return rowCnt, rows, pageSize, pageIndex, pageOffset