# coding:utf-8
import json

from volcengine.imagex.ImageXService import ImageXService


def describe_imagex_domain_traffic_data(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXDomainTrafficData', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXDomainTrafficData')
    res_json = json.loads(res)
    return res_json


def describe_imagex_domain_bandwidth_data(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXDomainBandwidthData', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXDomainBandwidthData')
    res_json = json.loads(res)
    return res_json


def describe_imagex_bucket_usage(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXBucketUsage', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXBucketUsage')
    res_json = json.loads(res)
    return res_json


def describe_imagex_request_cnt_usage(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXRequestCntUsage', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXRequestCntUsage')
    res_json = json.loads(res)
    return res_json


def describe_imagex_base_op_usage(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXBaseOpUsage', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXBaseOpUsage')
    res_json = json.loads(res)
    return res_json


def describe_imagex_compress_usage(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXCompressUsage', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXCompressUsage')
    res_json = json.loads(res)
    return res_json


def describe_imagex_edge_request(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXEdgeRequest', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXEdgeRequest')
    res_json = json.loads(res)
    return res_json


def describe_imagex_hit_rate_traffic_data(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXHitRateTrafficData', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXHitRateTrafficData')
    res_json = json.loads(res)
    return res_json


def describe_imagex_hit_rate_request_data(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXHitRateRequestData', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXHitRateRequestData')
    res_json = json.loads(res)
    return res_json


def describe_imagex_cdntop_request_data(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXCDNTopRequestData', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXCDNTopRequestData')
    res_json = json.loads(res)
    return res_json


def describe_imagex_summary(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXSummary', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXSummary')
    res_json = json.loads(res)
    return res_json


def describe_imagex_edge_request_bandwidth(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXEdgeRequestBandwidth', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXEdgeRequestBandwidth')
    res_json = json.loads(res)
    return res_json


def describe_imagex_edge_request_traffic(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXEdgeRequestTraffic', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXEdgeRequestTraffic')
    res_json = json.loads(res)
    return res_json


def describe_imagex_edge_request_regions(service: ImageXService, query):
    res = service.imagex_get('DescribeImageXEdgeRequestRegions', query)
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXEdgeRequestRegions')
    res_json = json.loads(res)
    return res_json


def describe_imagex_mirror_request_traffic(service: ImageXService, body):
    res = service.imagex_post('DescribeImageXMirrorRequestTraffic', [], json.dumps(body))
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestTraffic')
    res_json = json.loads(res)
    return res_json


def describe_imagex_mirror_request_bandwidth(service: ImageXService, body):
    res = service.imagex_post('DescribeImageXMirrorRequestBandwidth', [], json.dumps(body))
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestBandwidth')
    res_json = json.loads(res)
    return res_json


def describe_imagex_mirror_request_http_code_by_time(service: ImageXService, body):
    res = service.imagex_post('DescribeImageXMirrorRequestHttpCodeByTime', [], json.dumps(body))
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestHttpCodeByTime')
    res_json = json.loads(res)
    return res_json


def describe_imagex_mirror_request_http_code_overview(service: ImageXService, body):
    res = service.imagex_post('DescribeImageXMirrorRequestHttpCodeOverview', [], json.dumps(body))
    if res == '':
        raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestHttpCodeOverview')
    res_json = json.loads(res)
    return res_json
