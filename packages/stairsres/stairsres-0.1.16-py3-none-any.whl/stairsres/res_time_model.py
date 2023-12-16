import sys
import math
import scipy.stats as stats
from bamt.networks.continuous_bn import ContinuousBN


class ResTimeModel:
    def __init__(self, dbwrapper):
        self.wrapper = dbwrapper

    @staticmethod
    def nearest_value(precalculation: dict, volume_for_work: float, work_name: str) -> float:
        volumes = precalculation[work_name]
        result = min(volumes, key=lambda volume: abs(volume - volume_for_work))
        return result

    def get_resources_volumes(self, work_name, work_volume, resource_name=None) -> dict:
        precalc = self.wrapper.get_precalculation([work_name])
        if not precalc:
            return {}
        worker_reqs = {}
        worker_reqs['worker_reqs'] = []
        volume_for_work = self.nearest_value(precalc, work_volume, work_name)
        res = precalc[work_name][ volume_for_work]['10%'].keys() if resource_name is None else [resource_name]
        for r in res:
            resource_data = precalc[work_name][volume_for_work]
            min_res_value = math.ceil(resource_data['10%'][r])
            max_res_value = math.ceil(resource_data['90%'][r])
            volume = math.ceil(resource_data['50%'][r])
            min_res_value = max(min_res_value, 1)
            max_res_value = max(max_res_value, 1)
            volume = max(volume, 1)
            worker_reqs['worker_reqs'].append({'kind': r,
                                               'volume': volume,
                                               'min_count': min_res_value,
                                               'max_count': max_res_value})
        return worker_reqs

    def get_time(self, work_volume: dict, resources: dict, quantile: str) -> float:
        q = 0.5
        if quantile == '0.9':
            q = 0.1
        if quantile == '0.1':
            q = 0.9
        work_name = next(iter(work_volume))
        bn_params = self.wrapper.get_models(work_name)
        model_work_name, model_res_names = next((k, [r for r in bn_params['info']['types'] if '_prod' not in r]) for k in bn_params['info']['types'] if '_prod' in k)
        bn = ContinuousBN()
        bn.load(bn_params)
        test_data = {res_bn_name: resources[res_name] for res_bn_name in model_res_names for res_name in resources if res_name in res_bn_name}
        mu, var = bn.get_dist(model_work_name, test_data)
        prod = mu if var == 0 else work_volume[work_name] / 5 if math.isnan(mu) else stats.norm.ppf(q=q, loc=mu, scale=var)
        return max(math.ceil(work_volume[work_name] / max(prod, mu)), 1) + 4

    def estimate_time(self, work_unit, worker_list, mode='0.5'):
        if not worker_list:
            return 0
        work_name = work_unit['name']
        work_volume = work_unit['volume']
        res_dict = {req['name']: req['_count'] for req in worker_list}
        return self.get_time(work_volume={work_name: work_volume}, resources=res_dict, quantile=mode) 
