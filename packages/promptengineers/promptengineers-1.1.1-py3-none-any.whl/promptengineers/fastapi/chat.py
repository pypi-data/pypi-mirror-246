import ujson
import traceback

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import StreamingResponse

from promptengineers.fastapi.controllers import ChatController
from promptengineers.core.exceptions import ValidationException
from promptengineers.retrieval.factories.provider import VectorSearchProviderFactory
from promptengineers.models.request import ReqBodyChat, ReqBodyAgentChat, ReqBodyVectorstoreChat
from promptengineers.models.response import (ResponseChat, ResponseAgentChat, ResponseVectorstoreChat,
									RESPONSE_STREAM_AGENT_CHAT, RESPONSE_STREAM_VECTORSTORE_CHAT,
									RESPONSE_STREAM_CHAT)
from promptengineers.retrieval.strategies import VectorstoreContext
from promptengineers.core.utils import logger
from promptengineers.tools.utils import format_agent_actions

router = APIRouter()
TAG = "Chat"

def get_controller(request: Request) -> ChatController:
	return ChatController(request=request)

#################################################
# ChatGPT
#################################################
@router.post(
	"/chat",
	tags=[TAG],
	response_model=ResponseChat,
	responses={
		200: {
			"content": {
				"text/event-stream": {
					"example": RESPONSE_STREAM_CHAT
				}
			}
		}
	},
)
async def chat(
	body: ReqBodyChat,
	chat_controller: ChatController = Depends(get_controller),
):
	"""Chat endpoint."""
	try:
		logger.debug('[POST /chat] Query: %s', str(body))
		# You can use the stream variable in your function as needed
		if not body.stream:
			# Format Response
			result, cb = chat_controller.langchain_http_chat(
				messages=body.messages,
				model=body.model,
				temperature=body.temperature
			)
			data = ujson.dumps({
				'message': result,
				'usage': {
					'total_tokens': cb.total_tokens,
					'prompt_tokens': cb.prompt_tokens,
					'completion_tokens': cb.completion_tokens,
					'total_cost': cb.total_cost,
					'successful_requests': cb.successful_requests
				},
			})
			logger.debug('[POST /chat] Result: %s', str(data))
			return Response(
				content=data,
				media_type='application/json',
				status_code=200
			)

		return StreamingResponse(
			chat_controller.langchain_stream_chat(
				messages=body.messages,
				model=body.model,
				temperature=body.temperature
			),
			headers={
				"Cache-Control": "no-cache",
				"Connection": "keep-alive",
				"Content-Type": "text/event-stream",
			}
		)
	except Exception as err:
		tb = traceback.format_exc()
		logger.error("[routes.files.list_files] Exception: %s\n%s", err, tb)
		raise HTTPException(status_code=500, detail="Internal Server Error") from err



#################################################
# Langchain Agent
#################################################
@router.post(
	"/chat/agent",
	tags=[TAG],
	response_model=ResponseAgentChat,
	responses={
		200: {
			"content": {
				"text/event-stream": {
					"example": RESPONSE_STREAM_AGENT_CHAT
				}
			}
		}
	},
)
async def agent(
	request: Request,
	body: ReqBodyAgentChat,
	chat_controller: ChatController = Depends(get_controller),
):
	"""Chat endpoint."""
	try:
		vectorstore = None
		if body.retrieval.provider and body.retrieval.index:
			# Retrieve User Tokens
			user_id = getattr(request.state, "user_id", None)

			# Retreve Vectorstore
			vectorstore_strategy = VectorSearchProviderFactory.choose(
				provider=body.retrieval.provider,
				user_id=user_id,
				index_name=body.retrieval.index
			)
			vectostore_service = VectorstoreContext(vectorstore_strategy)
			vectorstore = vectostore_service.load()

		# You can use the stream variable in your function as needed
		if not body.stream:
			# Format Response
			result, cb = chat_controller.langchain_http_agent_chat(
				messages=body.messages,
				model=body.model,
				temperature=body.temperature,
				tools=body.tools,
				plugins=body.plugins,
				vectorstore=vectorstore,
			)
			data = ujson.dumps({
				'message': result['output'],
				'actions': format_agent_actions(result['intermediate_steps']),
				'usage': {
					'total_tokens': cb.total_tokens,
					'prompt_tokens': cb.prompt_tokens,
					'completion_tokens': cb.completion_tokens,
					'total_cost': cb.total_cost,
					'successful_requests': cb.successful_requests
				},
			})
			logger.debug('[POST /chat/agent] Result: %s', str(data))
			return Response(
				content=data,
				media_type='application/json',
				status_code=200
			)

		return StreamingResponse(
			chat_controller.langchain_stream_agent_chat(
				messages=body.messages,
				model=body.model,
				temperature=body.temperature,
				tools=body.tools,
				plugins=body.plugins,
				vectorstore=vectorstore,
			),
			headers={
				"Cache-Control": "no-cache",
				"Connection": "keep-alive",
				"Content-Type": "text/event-stream",
			}
		)
	except Exception as err:
		tb = traceback.format_exc()
		logger.error("[routes.chat.vector_search] Exception: %s\n%s", err, tb)
		raise HTTPException(status_code=500, detail="Internal Server Error") from err

#################################################
# Langchain Vectorstore Route
#################################################
@router.post(
	"/chat/vectorstore",
	tags=[TAG],
	response_model=ResponseVectorstoreChat,
	responses={
		200: {
			"content": {
				"text/event-stream": {
					"example": RESPONSE_STREAM_VECTORSTORE_CHAT
				}
			}
		}
	},
)
async def vector_search(
	request: Request,
	body: ReqBodyVectorstoreChat,
	chat_controller: ChatController = Depends(get_controller),
):
	"""Chat Vectorstore endpoint."""
	try:
		# Log Context Details
		logger.debug('[POST /chat/vectorstore] Query: %s', str(body))

		# Retrieve User Tokens
		user_id = getattr(request.state, "user_id", None)

		# Retreve Vectorstore
		vectorstore_strategy = VectorSearchProviderFactory.choose(
			provider=body.provider,
			user_id=user_id,
			index_name=body.vectorstore
		)
		vectostore_service = VectorstoreContext(vectorstore_strategy)
		vectorstore = vectostore_service.load()

		# Check if the retrieved file is empty
		if not vectorstore:
			raise HTTPException(
				status_code=404,
				detail=f"Vectorstore {body.vectorstore} not found"
			)

		# You can use the stream variable in your function as needed
		if not body.stream:
			# Format Response
			result, cb = chat_controller.langchain_http_vectorstore_chat(
				messages=body.messages,
				model=body.model,
				temperature=body.temperature,
				vectorstore=vectorstore,
			)
			data = ujson.dumps({
				'message': result['answer'],
				'documents': result['source_documents'],
				'usage': {
					'total_tokens': cb.total_tokens,
					'prompt_tokens': cb.prompt_tokens,
					'completion_tokens': cb.completion_tokens,
					'total_cost': cb.total_cost,
					'successful_requests': cb.successful_requests
				},
			})
			logger.debug('[POST /chat/vectorstore] Result: %s', str(data))
			return Response(
				content=data,
				media_type='application/json',
				status_code=200
			)

		# Process Query
		return StreamingResponse(
			chat_controller.langchain_stream_vectorstore_chat(
				messages=body.messages,
				model=body.model,
				temperature=body.temperature,
				vectorstore=vectorstore,
			),
			media_type="text/event-stream"
		)
	except ValidationException as err:
		logger.warning("[routes.chat.vector_search] ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except HTTPException as err:
		logger.error("[routes.chat.vector_search] HTTPException: %s", err.detail)
		raise
	except Exception as err:
		tb = traceback.format_exc()
		logger.error("[routes.chat.vector_search] Exception: %s\n%s", err, tb)
		raise HTTPException(status_code=500, detail="Internal Server Error") from err
