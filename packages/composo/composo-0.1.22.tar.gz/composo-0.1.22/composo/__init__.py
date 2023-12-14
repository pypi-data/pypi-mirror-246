_D='PACKAGE_ENV'
_C='prod'
_B=True
_A=None
__version__='0.1.22'
import os,inspect,copy,time,math,json
from typing import List,Union,Any,Literal
import requests
from.package_schemas import*
import logging
from colorama import init,Fore
init()
class ComposoLogHandler(logging.StreamHandler):
	def __new__(cls,*args,**kwargs):return super(ComposoLogHandler,cls).__new__(cls)
	def __init__(self,stream=_A):super().__init__(stream)
	def emit(self,record):record.msg=f"{Fore.BLUE}Composo:{Fore.RESET} {record.msg}";super().emit(record)
logger=logging.getLogger('ComposoLogger')
if os.environ.get(_D,_C)in['local','dev']:print("Using DEBUG logging as you're running locally");logger.setLevel(logging.DEBUG)
else:logger.setLevel(logging.INFO)
handler=ComposoLogHandler()
formatter=logging.Formatter('%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
class ComposoException(Exception):0
class ComposoUserException(ComposoException):0
class ComposoCriticalException(ComposoException):0
class ComposoDeveloperException(ComposoException):0
class StrParam(str):
	def __new__(cls,description=_A,*args,**kwargs):obj=super().__new__(cls,*args,**kwargs);obj.description=description;return obj
	def get_constraint_string(self):0
	def validate(self,item):0
	@staticmethod
	def type_string():return DataType.STRING.name
class IntParam(int):
	def __new__(cls,description=_A,min=_A,max=_A,*args,**kwargs):obj=super().__new__(cls,*args,**kwargs);obj.description=description;obj.min=min;obj.max=max;return obj
	def get_constraint_string(self):
		constraint_str=''
		if self.min is not _A:
			constraint_str+=f"min:{str(self.min)}"
			if self.max is not _A:constraint_str+='; '
		if self.max is not _A:constraint_str+=f"max:{str(self.max)}"
		return constraint_str
	def validate(self,value):
		if self.min and not value>=self.min:raise ComposoUserException(f"Parameter is invalid. Value {value} does not exceed minimum value: {self.min}")
		if self.max and not value<=self.max:raise ComposoUserException(f"Parameter is invalid. Value {value} exceeds maximum value: {self.max}")
		return _B
	@staticmethod
	def type_string():return DataType.INTEGER.name
class FloatParam(float):
	def __new__(cls,description=_A,min=_A,max=_A,*args,**kwargs):obj=super().__new__(cls,*args,**kwargs);obj.description=description;obj.min=min;obj.max=max;return obj
	def get_constraint_string(self):
		constraint_str=''
		if self.min is not _A:
			constraint_str+=f"min:{str(self.min)}"
			if self.max is not _A:constraint_str+='; '
		if self.max is not _A:constraint_str+=f"max:{str(self.max)}"
		return constraint_str
	def validate(self,value):
		if self.min and not value>=self.min:raise ComposoUserException(f"Parameter is invalid. Value {value} does not exceed minimum value: {self.min}")
		if self.max and not value<=self.max:raise ComposoUserException(f"Parameter is invalid. Value {value} exceeds maximum value: {self.max}")
		return _B
	@staticmethod
	def type_string():return DataType.FLOAT.name
class MultiChoiceStrParam(str):
	def __new__(cls,choices=_A,description=_A,*args,**kwargs):obj=super().__new__(cls,*args,**kwargs);obj.description=description;obj.choices=choices;return obj
	def get_constraint_string(self):return f"options: {'; '.join(self.choices)}"
	def validate(self,value):
		if self.choices is not _A:
			if value not in self.choices:raise ComposoUserException(f"Parameter is invalid. Value {value} is not in the list of allowable values: {self.choices}")
		return _B
	@staticmethod
	def type_string():return DataType.MULTICHOICESTRING.name
WORKABLE_TYPES=Union[StrParam,IntParam,FloatParam,MultiChoiceStrParam]
class BackendEventGress:
	backend_url:0
	def __init__(self,app_registration):
		self.app_registration=app_registration
		if os.environ.get(_D,_C)=='local':logger.info('Connecting to Composo local');self.backend_url='http://localhost:8000'
		elif os.environ.get(_D,_C)=='dev':logger.info('Connecting to Composo dev');self.backend_url='https://composo-prod-backend-composo-dev-backend.azurewebsites.net'
		elif os.environ.get(_D,_C)=='test':logger.info('Connecting to Composo test');self.backend_url='http://composo-prod-backend-composo-test-backend.azurewebsites.net'
		else:self.backend_url='https://composo.ai'
	@staticmethod
	def is_valid_json(data):
		import json
		try:json.loads(data);return _B
		except Exception:return False
	def make_request(self,method,path,data=_A):
		logger.debug(f"Request started path: {path}")
		if not type(data)==dict or data is _A:raise ComposoDeveloperException("Data must be a dict or None. Something's gone wrong.")
		jsondump=json.dumps(data,default=str);headers={'Content-Type':'application/json'};url=self.backend_url+path;tries=0;max_tries=100
		while tries<max_tries:
			try:
				if method.lower()=='post':response=requests.post(url,data=jsondump,headers=headers,timeout=100)
				elif method.lower()=='get':response=requests.get(url,headers=headers,timeout=100)
				elif method.lower()=='put':response=requests.put(url,data=jsondump,headers=headers,timeout=100)
				else:raise ValueError('Invalid method. Available options are "post", "get", and "put".')
				if tries>0:logger.info('Connection to Composo backend re-established')
				logger.debug(f"Request finished path: {path}");return response
			except requests.exceptions.Timeout as e:logger.info(f"Request to Composo timed out. Retry {tries+1} of {max_tries}");time.sleep(max(10*(tries/10)**2,10));tries+=1
			except requests.exceptions.ConnectionError as e:logger.info(f"Could not connect to Composo. Retry {tries+1} of {max_tries}");time.sleep(max(10*(tries/10)**2,10));tries+=1
			except Exception as e:raise ComposoDeveloperException(f"There was an unexpected error in backend polling: {str(e)}")
		raise ComposoCriticalException(f"Could not connect to Composo backend after {max_tries} tries.")
class LiveEventIngress(BackendEventGress):
	def event_poll(self):
		A='message';response=self.make_request(method='post',path='/api/runner',data=self.app_registration.dict())
		if response.status_code==200:
			json_response=response.json()
			for event_type in[PollResponse,AppDeletionEvent]:
				try:parsed_event=event_type.parse_obj(json_response);return parsed_event
				except Exception as e:pass
			raise ComposoDeveloperException(f"Could not parse the response from the backend into a known response type: {response}")
		elif response.status_code==418:logger.error(f"ERROR: {response.json()[A]}")
		elif response.status_code==501:ComposoDeveloperException(f"POLLING ERROR: {response.json()[A]}")
		else:raise ComposoDeveloperException(f"The backend is returning an unknown error from polling: {response}")
class LiveEventEgress(BackendEventGress):
	def report_run_results(self,run_result,run_id):
		response=self.make_request('put',path=f"/api/runner/{run_id}",data=run_result.dict())
		if response.status_code==200:logger.info('Run completed and results reported')
		else:raise ComposoDeveloperException(f"The backend is returning a non 200 status code from reporting run results, this should never happen: {response}")
def match_parameters(func,*args,**kwargs):
	signature=inspect.signature(func);parameters=signature.parameters;matched_params={}
	for(i,param_name)in enumerate(parameters.keys()):
		if i<len(args):matched_params[param_name]=args[i]
		elif param_name in kwargs:matched_params[param_name]=kwargs[param_name]
		elif parameters[param_name].default is not inspect.Parameter.empty:matched_params[param_name]=parameters[param_name].default
		else:raise TypeError(f"Missing required argument '{param_name}'")
	return matched_params
def experiment_controller(func,demo_args,demo_kwargs,demo_globals,api_key='cp-XXX_FAKE_KEY_FOR_TESTING_XXXX',event_ingress=_A,event_egress=_A,poll_wait_time=3):
	'\n    Args:\n        event_ingress (_type_): server-side events from polling\n        event_egress (_type_): various backend methods\n\n    ';L='any';K='boolean';J='str_type';I='string';H='constraints';G='description';F='instantiated_type';E='is_kwarg';D='demo';C='is_fixed';B='name';A='type';logger.info('Composo Experiment is activated');vars_format_schema={A:'array','items':{A:'object','properties':{B:{A:I},E:{A:K},C:{A:K},F:{A:L},A:{A:L},J:{A:I},G:{A:I},D:{A:I},H:{A:I}},'required':[B,A,G,D,H]}};all_demos=match_parameters(func,*demo_args,**demo_kwargs);signature=inspect.signature(func);inspected_args={param.name:param.annotation for param in signature.parameters.values()if param.default==inspect.Parameter.empty};inspected_kwargs={param.name:param.annotation for param in signature.parameters.values()if param.default!=inspect.Parameter.empty};all_vars=[]
	for(name,_type)in{**inspected_args,**inspected_kwargs}.items():
		is_kwarg=name in inspected_kwargs.keys()
		if _type in WORKABLE_TYPES.__args__ or type(_type)in WORKABLE_TYPES.__args__:
			is_fixed=False
			try:this_arg_type=_type.__bases__[0];description=_A;constraint_string=_A;instantiated_type=_A
			except AttributeError as e:this_arg_type=type(_type).__bases__[0];description=_type.description;constraint_string=_type.get_constraint_string();instantiated_type=_type
			str_type=_type.type_string();all_vars.append({B:name,E:is_kwarg,C:is_fixed,F:instantiated_type,A:this_arg_type,J:str_type,G:description,D:all_demos[name],H:constraint_string})
		else:is_fixed=_B;all_vars.append({B:name,E:is_kwarg,C:is_fixed,F:_A,A:_A,J:_A,G:_A,D:all_demos[name],H:_A})
	app_registration=AppRegistration(api_key=api_key,runner_type='python',runner_version=__version__,parameters=[x[B]for x in all_vars if not x[C]],types=[x[J]for x in all_vars if not x[C]],demo_values=[json.dumps(x[D])for x in all_vars if not x[C]],descriptions=[x[G]for x in all_vars if not x[C]],constraints=[x[H]for x in all_vars if not x[C]])
	if event_ingress is _A or event_egress is _A:
		logger.info('Initialising live connection to Composo')
		if api_key is _A:raise ValueError('api_key must be provided')
		event_ingress=LiveEventIngress(app_registration);event_egress=LiveEventEgress(app_registration)
	elif event_ingress is _A and event_egress is not _A or event_ingress is not _A and event_egress is _A:raise ValueError('event_ingress and event_egress must both be None or both be not None')
	def run_experiment(replacement_vars):
		'\n        Takes a dict where both keys and values are strings, conversion to the correct type is handled inside\n        \n        ';C='working_value';logger.info('Experiment initiated')
		if not all(key in[x[B]for x in all_vars]for key in replacement_vars.keys()):raise ComposoDeveloperException(f"The user has somehow been allowed to provide args that are not tagged. Provided args: {replacement_vars.keys()}. Tagged args: {[x[B]for x in all_vars]} ")
		working_all_vars=copy.deepcopy(all_vars)
		for i in range(len(working_all_vars)):working_all_vars[i][C]=working_all_vars[i][D]
		for(arg_name,arg_value)in replacement_vars.items():
			this_var=[x for x in all_vars if x[B]==arg_name][0]
			try:typed_value=this_var[A](arg_value)
			except Exception as e:raise ComposoUserException(f"The provided arg could not be converted to required type: {this_var[A]}. Arg value was {arg_value}")
			if this_var[F]is not _A:this_var[F].validate(typed_value)
			all_var_index=[i for(i,x)in enumerate(working_all_vars)if x[B]==arg_name][0];working_all_vars[all_var_index][C]=typed_value
		working_args=[x[C]for x in working_all_vars if not x[E]];working_kwargs={x[B]:x[C]for x in working_all_vars if x[E]}
		try:ret_val=func(*working_args,**working_kwargs)
		except Exception as e:raise ComposoUserException(f"The linked function produced an error: {str(e)}")
		return ret_val
	previously_noted_app_ids=[];logger.info('Connected and listening.')
	while _B:
		try:
			time.sleep(poll_wait_time);event=event_ingress.event_poll()
			if isinstance(event,PollResponse):
				if isinstance(event.payload,AppDeletionEvent):logger.critical('Composo is shutting down.');logger.critical(event.payload.message);return
				registered_apps=event.registered_apps
				for registered_app in registered_apps:
					if registered_app not in previously_noted_app_ids:logger.info(f"App registered: {registered_app}");previously_noted_app_ids.append(registered_app)
				if event.payload is not _A:
					logger.info('New Evaluation Run Triggered');case_results=[];logger.info(f"Running {len(event.payload.cases)} cases")
					for(i,case)in enumerate(event.payload.cases):
						case_result=_A
						try:ret=run_experiment(case.vars);ret_type=type(ret);enum_type=native_type_to_enum[ret_type].value;case_result=CaseResult(case_id=case.case_id,value=json.dumps(ret),value_type=enum_type,error=_A);case_results.append(case_result)
						except ComposoUserException as e:case_result=CaseResult(case_id=case.case_id,value=_A,value_type=_A,error='ERROR: '+str(e));case_results.append(case_result)
						except Exception as e:
							if os.environ.get(_D,_C)!=_C:logger.debug(f"Unidentified exception caught with case {case}: {str(e)}")
							case_result=CaseResult(case_id=case.case_id,value=_A,value_type=_A,error='ERROR: The composo package has failed with an unidentified error. Please contact composo support.');case_results.append(case_result)
						print('Case run successfully');event_egress.report_run_results(RunResult(run_id=event.payload.run_id,results=case_results),run_id=event.payload.run_id)
		except ComposoDeveloperException as e:logger.debug(f"Composo Developer Exception caught: {str(e)}");pass
		except ComposoUserException as e:logger.info(f"Composo User Exception caught: {str(e)}")
		except ComposoCriticalException as e:raise e
		except Exception as e:print(e);logger.debug(f"Unidentified exception caught: {str(e)}");pass
def generate_api_key():import secrets,string;key_length=32;characters=string.ascii_uppercase+string.digits;api_key=''.join(secrets.choice(characters)for _ in range(key_length-3));api_key='cp-'+api_key;return api_key
class Composo:
	@classmethod
	def link(cls,api_key=_A):
		cls.api_key=api_key
		def actual_decorator(func):
			def wrapped_func(*args,**kwargs):
				B='########################################';A='COMPOSO_APP_API_KEY'
				if not hasattr(Composo,'activated'):
					cls.activated=_B
					if cls.api_key is _A:
						if A in os.environ:api_key=os.environ[A]
						else:api_key=generate_api_key()
					else:api_key=cls.api_key
					logger.info(B);logger.info('######### Your Composo API Key #########');logger.info('### '+api_key+' ###');logger.info(B)
					try:result=func(*args,**kwargs)
					except Exception as e:raise Exception('The function invocation has errors. Please fix before linking to Composo. Error: '+str(e))
					permissable_return_types=[int,float,str];result_type=type(result)
					if result_type not in permissable_return_types:raise Exception(f"The linked function returned type: {result_type}. Supported return types are {', '.join([x.__name__ for x in permissable_return_types])}")
					experiment_controller(func,args,kwargs,func.__globals__,api_key=api_key);return result
				else:result=func(*args,**kwargs)
			return wrapped_func
		return actual_decorator