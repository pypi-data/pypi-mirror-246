_G='nullable'
_F='precision'
_E='length'
_D='table_name'
_C='schema_name'
_B='type'
_A='name'
import re
from abc import ABC,abstractmethod
from localstack.utils.objects import get_all_subclasses
from simple_ddl_parser import DDLParser
from snowflake_local.engine.models import Query
from snowflake_local.server.conversions import to_pyarrow_table_bytes_b64
from snowflake_local.server.models import QueryResponse
class QueryResultPostprocessor(ABC):
	def should_apply(A,query,result):return True
	@abstractmethod
	def apply(self,query,result):0
class FixShowSchemasResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*SHOW\\s+.*SCHEMAS',query.original_query,flags=re.I))
	def apply(A,query,result):_replace_dict_value(result.data.rowtype,_A,_C,_A)
class FixShowObjectsResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*SHOW\\s+.*OBJECTS',query.original_query,flags=re.I))
	def apply(B,query,result):A=result;_replace_dict_value(A.data.rowtype,_A,'table_schema',_C);_replace_dict_value(A.data.rowtype,_A,_D,_A);_replace_dict_value(A.data.rowtype,_A,'table_type','kind');_replace_dict_value(A.data.rowtype,_A,'table_catalog','database_name')
class FixCreateTableResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(_get_table_from_creation_query(query.original_query))
	def apply(C,query,result):A=result;B=_get_table_from_creation_query(query.original_query);A.data.rowset.append([f"Table {B} successfully created."]);A.data.rowtype.append({_A:'status',_B:'text',_E:-1,_F:0,'scale':0,_G:True})
class FixInsertQueryResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*INSERT\\s+.+',query.original_query,flags=re.I))
	def apply(B,query,result):A=result;A.data.rowset=[[len(A.data.rowset)]];A.data.rowtype.append({_A:'count',_B:'integer',_E:-1,_F:0,'scale':0,_G:True})
class UpdateSessionAfterCreatingDatabase(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+DATABASE(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.database=C.group(2);A.session.schema=None
class UpdateSessionAfterCreatingSchema(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+SCHEMA(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.schema=C.group(2)
class AdjustQueryResultFormat(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('.+FROM\\s+@',query.original_query,flags=re.I);A.data.queryResultFormat='arrow'if B else'json'
		if B:A.data.rowsetBase64=to_pyarrow_table_bytes_b64(A);A.data.rowset=[];A.data.rowtype=[]
class AdjustColumnTypes(QueryResultPostprocessor):
	TYPE_MAPPINGS={'UNKNOWN':'TEXT'}
	def apply(C,query,result):
		for A in result.data.rowtype:
			D=A.get(_B,'');B=C.TYPE_MAPPINGS.get(D)
			if B:A[_B]=B
class ReturnDescribeTableError(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('desc(?:ribe)?\\s+.+',query.original_query,flags=re.I)
		if B and not A.data.rowset:A.success=False
def apply_post_processors(query,result):
	B=result;A=query
	for D in get_all_subclasses(QueryResultPostprocessor):
		C=D()
		if C.should_apply(A,result=B):C.apply(A,result=B)
def _replace_dict_value(values,attr_key,attr_value,attr_value_replace):
	A=attr_key;B=[B for B in values if B[A]==attr_value]
	if B:B[0][A]=attr_value_replace
def _get_table_from_creation_query(query):
	A=DDLParser(query).run()
	if not A:return
	B=A[0].get(_D)
	if B and not A[0].get('alter'):return B