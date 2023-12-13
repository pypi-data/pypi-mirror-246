import requests
import pandas as pd
import json
from retry import retry


@retry(tries=10, delay=2, backoff=2)
def warning_investigation(url, headers, appCode, pageNum="1", pageSize="1000", dcInFarmName="*", wfFarmName="*",
                          scadaFarmName="*", fanCode="*", scadaFanSeat="*", startdataStartTime="00010101",
                          enddataStartTime="99991231", startdataEndTime="00010101", enddataEndTime="99991231",
                          startmodelExecutionTime="00010101", endmodelExecutionTime="99991231",
                          startrequireFinishDate="00010101", endrequireFinishDate="99991231", startreviewTime="00010101",
                          endreviewTime="99991231", startapplyIssueTime="00010101", endapplyIssueTime="99991231",
                          startdeliverSiteTime="00010101", enddeliverSiteTime="99991231", startinvestigate_date="00010101",
                          endinvestigate_date="99991231", startverification_time="00010101", endverification_time="99991231",
                          dcInFanSeat="*", dcModelName="*", hascheck="*", warningAccurate="*", problemsFound="*",
                          startapplyTime="00010101", endapplyTime="99991231"):
    """
    调用warning_investigation接口
    :param: url:
    :param headers:
    :param appCode:
    :param pageNum: 页编号
    :param pageSize: 页大小
    :param dcInFarmName:风场名（内）
    :param wfFarmName:风场名（外）
    :param scadaFarmName:风场名（SCADA）
    :param dcInFanSeat:风机号（内）
    :param fanCode:风机号（外）
    :param scadaFanSeat:风机号（SCADA）
    :param dcModelName:模型名称（英）
    :param hascheck:是否执行过排查
    :param warningAccurate:是否预警准确
    :param problemsFound:排查发现问题点
    :param startdataStartTime:开始-数据开始时间
    :param startdataEndTime:开始-数据结束时间
    :param startmodelExecutionTime:开始-模型执行时间
    :param startapplyTime:开始-申请排查时间
    :param startrequireFinishDate:开始-要求完成时间
    :param startreviewTime:开始-排查审核时间
    :param startapplyIssueTime:开始-下发审核时间
    :param startdeliverSiteTime:开始-下发现场时间
    :param startinvestigate_date:开始-执行排查办理时间
    :param startverification_time:开始-模型验证时间
    :param enddataStartTime:结束-数据开始时间
    :param enddataEndTime:结束-数据结束时间
    :param endmodelExecutionTime:结束-模型执行时间
    :param endapplyTime:结束-申请排查时间
    :param endrequireFinishDate:结束-要求完成时间
    :param endreviewTime:结束-排查审核时间
    :param endapplyIssueTime:结束-下发审核时间
    :param enddeliverSiteTime:结束-下发现场时间
    :param endinvestigate_date:结束-执行排查办理时间
    :param endverification_time:结束-模型验证时间
    :return: status 返回的状态， 成功或报错信息；
            data 返回的数据；
            totalNum 查到的数据量
    """
    params ="appCode={appCode}&"\
            "dcInFarmName={dcInFarmName}&"\
            "pageNum={pageNum}&"\
            "pageSize={pageSize}&"\
            "wfFarmName={wfFarmName}&"\
            "scadaFarmName={scadaFarmName}&"\
            "fanCode={fanCode}&"\
            "scadaFanSeat={scadaFanSeat}&"\
            "startdataStartTime={startdataStartTime}&"\
            "enddataStartTime={enddataStartTime}&"\
            "startdataEndTime={startdataEndTime}&"\
            "enddataEndTime={enddataEndTime}&"\
            "startmodelExecutionTime={startmodelExecutionTime}&"\
            "endmodelExecutionTime={endmodelExecutionTime}&"\
            "startrequireFinishDate={startrequireFinishDate}&"\
            "endrequireFinishDate={endrequireFinishDate}&"\
            "startreviewTime={startreviewTime}&"\
            "endreviewTime={endreviewTime}&"\
            "startapplyIssueTime={startapplyIssueTime}&"\
            "endapplyIssueTime={endapplyIssueTime}&"\
            "startdeliverSiteTime={startdeliverSiteTime}&"\
            "enddeliverSiteTime={enddeliverSiteTime}&"\
            "startinvestigate_date={startinvestigate_date}&"\
            "endinvestigate_date={endinvestigate_date}&"\
            "startverification_time={startverification_time}&"\
            "endverification_time={endverification_time}&"\
            "dcInFanSeat={dcInFanSeat}&"\
            "dcModelName={dcModelName}&"\
            "hascheck={hascheck}&"\
            "warningAccurate={warningAccurate}&"\
            "problemsFound={problemsFound}&"\
            "startapplyTime={startapplyTime}&"\
            "endapplyTime={endapplyTime}"
    params = params.format(appCode=appCode, pageNum=pageNum, pageSize=pageSize, dcInFarmName=dcInFarmName, wfFarmName=wfFarmName, scadaFarmName=scadaFarmName,
                           fanCode=fanCode, scadaFanSeat=scadaFanSeat, startdataStartTime=startdataStartTime,enddataStartTime=enddataStartTime, startdataEndTime=startdataEndTime,
                           enddataEndTime=enddataEndTime, startmodelExecutionTime=startmodelExecutionTime, endmodelExecutionTime=endmodelExecutionTime, startrequireFinishDate=startrequireFinishDate,
                           endrequireFinishDate=endrequireFinishDate, startreviewTime=startreviewTime, endreviewTime=endreviewTime, startapplyIssueTime=startapplyIssueTime,
                           endapplyIssueTime=endapplyIssueTime, startdeliverSiteTime=startdeliverSiteTime, enddeliverSiteTime=enddeliverSiteTime, startinvestigate_date=startinvestigate_date,
                           endinvestigate_date=endinvestigate_date, startverification_time=startverification_time, endverification_time=endverification_time, dcInFanSeat=dcInFanSeat, dcModelName=dcModelName,
                           hascheck=hascheck, warningAccurate=warningAccurate, problemsFound=problemsFound, startapplyTime=startapplyTime, endapplyTime=endapplyTime)
    url_address = url + '?' + params
    check_data = requests.post(url=url_address, headers=headers, timeout=10)
    DOM_result = json.loads(check_data.text)
    if DOM_result['errMsg'] == 'success':

        return 'success', pd.DataFrame(DOM_result['data']['rows']), float(DOM_result['data']['totalNum'])
    else:
        print('请求参数异常:', DOM_result['errMsg'])
        return DOM_result['errMsg'], None, None


@retry(tries=10, delay=2, backoff=2)
def cm_intelligent_plan(url, headers, appCode, wf_farm_code,  pageNum="1", pageSize="1000", inner_turbine_code="*",
                          check_name="*", start_time="00010101", end_time="99991231"):
    """
    调用cm_intelligent_plan接口
    :param url:
    :param headers:
    :param appCode:
    :param pageNum: 页编号
    :param pageSize: 页大小
    :param wf_farm_code:风场编号
    :param inner_turbine_code:业主机位号（内部）
    :param check_name:检查项目
    :param start_time:检查日期check_time的开始时间
    :param end_time:检查日期check_time的结束时间
    :return: status 返回的状态， 成功或报错信息；
            data 返回的数据；
            totalNum 查到的数据量
    """
    params ="appCode={appCode}&"\
            "pageNum={pageNum}&"\
            "pageSize={pageSize}&"\
            "wf_farm_code={wf_farm_code}&"\
            "inner_turbine_code={inner_turbine_code}&"\
            "check_name={check_name}&"\
            "start_time={start_time}&"\
            "end_time={end_time}"
    params = params.format(appCode=appCode, pageNum=pageNum, pageSize=pageSize, wf_farm_code=wf_farm_code,
                           inner_turbine_code=inner_turbine_code, check_name=check_name, start_time=start_time,
                           end_time=end_time)
    url_address = url + '?' + params
    check_data = requests.post(url=url_address, headers=headers, timeout=10)
    DOM_result = json.loads(check_data.text)
    if DOM_result['errMsg'] == 'success':
        return 'success', pd.DataFrame(DOM_result['data']['rows']), float(DOM_result['data']['totalNum'])
    else:
        print('请求参数异常:', DOM_result['errMsg'])
        return DOM_result['errMsg'], None, None



