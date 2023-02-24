# coding:utf-8
from volcengine.ApiInfo import ApiInfo
from volcengine.imagex.ImageXConfig import api_info, IMAGEX_API_VERSION


def init():
    for v in ["DescribeImageXDomainTrafficData",
              "DescribeImageXDomainBandwidthData",
              "DescribeImageXBucketUsage",
              "DescribeImageXRequestCntUsage",
              "DescribeImageXBaseOpUsage",
              "DescribeImageXCompressUsage",
              "DescribeImageXEdgeRequest",
              "DescribeImageXHitRateTrafficData",
              "DescribeImageXHitRateRequestData",
              "DescribeImageXCDNTopRequestData",
              "DescribeImageXSummary",
              "DescribeImageXEdgeRequestBandwidth",
              "DescribeImageXEdgeRequestTraffic",
              "DescribeImageXEdgeRequestRegions",
              ]:
        api_info[v] = ApiInfo("GET", "/", {"Action": v, "Version": IMAGEX_API_VERSION}, {}, {})

    for v in ["DescribeImageXMirrorRequestTraffic",
              "DescribeImageXMirrorRequestBandwidth",
              "DescribeImageXMirrorRequestHttpCodeByTime",
              "DescribeImageXMirrorRequestHttpCodeOverview",
              ]:
        api_info[v] = ApiInfo("POST", "/", {"Action": v, "Version": IMAGEX_API_VERSION}, {}, {})


init()
