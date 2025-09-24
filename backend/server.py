I'll provide you with the complete code for the entire CarCommunity app. Here are all the files you need:
Action: file_editor view /app/backend/server.py
Observation: /app/backend/server.py:
1|from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, Cookie, Response
2|from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
3|from dotenv import load_dotenv
4|from starlette.middleware.cors import CORSMiddleware
5|from motor.motor_asyncio import AsyncIOMotorClient
6|import os
7|import logging
8|from pathlib import Path
9|from pydantic import BaseModel, Field, EmailStr
10|from typing import List, Optional
11|import uuid
12|from datetime import datetime, timezone, timedelta
13|import requests
14|
15|ROOT_DIR = Path(__file__).parent
16|load_dotenv(ROOT_DIR / '.env')
17|
18|# MongoDB connection
19|mongo_url = os.environ['MONGO_URL']
20|client = AsyncIOMotorClient(mongo_url)
21|db = client[os.environ['DB_NAME']]
22|
23|# Create the main app without a prefix
24|app = FastAPI()
25|
26|# Create a router with the /api prefix
27|api_router = APIRouter(prefix="/api")
28|
29|# Security
30|security = HTTPBearer(auto_error=False)
31|
32|# Auth configuration - no instance needed, using direct API calls
33|
34|# Models
35|class User(BaseModel):
36|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
37|    email: str
38|    name: str
39|    picture: Optional[str] = None
40|    bio: Optional[str] = None
41|    car_info: Optional[str] = None
42|    location: Optional[str] = None
43|    followers_count: int = 0
44|    following_count: int = 0
45|    posts_count: int = 0
46|    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
47|
48|class UserCreate(BaseModel):
49|    email: str
50|    name: str
51|    picture: Optional[str] = None
52|
53|class UserUpdate(BaseModel):
54|    name: Optional[str] = None
55|    bio: Optional[str] = None
56|    car_info: Optional[str] = None
57|    location: Optional[str] = None
58|
59|class Post(BaseModel):
60|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
61|    user_id: str
62|    content: str
63|    image_url: Optional[str] = None
64|    video_url: Optional[str] = None
65|    build_category: Optional[str] = None
66|    likes_count: int = 0
67|    comments_count: int = 0
68|    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
69|    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
70|
71|class PostCreate(BaseModel):
72|    content: str
73|    image_url: Optional[str] = None
74|    video_url: Optional[str] = None
75|    build_category: Optional[str] = None
76|
77|class Comment(BaseModel):
78|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
79|    post_id: str
80|    user_id: str
81|    content: str
82|    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
83|
84|class CommentCreate(BaseModel):
85|    content: str
86|
87|class Like(BaseModel):
88|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
89|    post_id: str
90|    user_id: str
91|    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
92|
93|class Follow(BaseModel):
94|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
95|    follower_id: str
96|    following_id: str
97|    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
98|
99|class SessionData(BaseModel):
100|    session_token: str
101|    user_id: str
102|    expires_at: datetime
103|
104|class PostWithUser(BaseModel):
105|    id: str
106|    user_id: str
107|    user_name: str
108|    user_picture: Optional[str]
109|    content: str
110|    image_url: Optional[str] = None
111|    video_url: Optional[str] = None
112|    build_category: Optional[str] = None
113|    likes_count: int
114|    comments_count: int
115|    is_liked: bool = False
116|    created_at: datetime
117|
118|# Authentication helpers
119|async def get_current_user(
120|    response: Response,
121|    session_token: Optional[str] = Cookie(None, alias="session_token"),
122|    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
123|) -> User:
124|    token = session_token
125|    if not token and credentials:
126|        token = credentials.credentials
127|    
128|    if not token:
129|        raise HTTPException(status_code=401, detail="Not authenticated")
130|    
131|    # Check session in database
132|    session = await db.sessions.find_one({"session_token": token})
133|    if not session or session["expires_at"] < datetime.now(timezone.utc):
134|        if session:
135|            await db.sessions.delete_one({"session_token": token})
136|        response.delete_cookie("session_token")
137|        raise HTTPException(status_code=401, detail="Session expired")
138|    
139|    # Get user
140|    user = await db.users.find_one({"id": session["user_id"]})
141|    if not user:
142|        raise HTTPException(status_code=404, detail="User not found")
143|    
144|    return User(**user)
145|
146|# Auth routes
147|@api_router.get("/auth/session")
148|async def get_session_data(session_id: str):
149|    """Get user data from session_id"""
150|    try:
151|        # Call Emergent Auth API
152|        response = requests.get(
153|            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
154|            headers={"X-Session-ID": session_id}
155|        )
156|        
157|        if response.status_code != 200:
158|            raise HTTPException(status_code=400, detail="Invalid session ID")
159|        
160|        data = response.json()
161|        
162|        # Check if user exists
163|        existing_user = await db.users.find_one({"email": data["email"]})
164|        
165|        if existing_user:
166|            user = User(**existing_user)
167|        else:
168|            # Create new user
169|            user_data = UserCreate(
170|                email=data["email"],
171|                name=data["name"],
172|                picture=data.get("picture")
173|            )
174|            user = User(**user_data.dict())
175|            await db.users.insert_one(user.dict())
176|        
177|        # Store session
178|        session_data = SessionData(
179|            session_token=data["session_token"],
180|            user_id=user.id,
181|            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
182|        )
183|        await db.sessions.insert_one(session_data.dict())
184|        
185|        return {
186|            "user": user,
187|            "session_token": data["session_token"]
188|        }
189|        
190|    except Exception as e:
191|        raise HTTPException(status_code=500, detail=str(e))
192|
193|@api_router.post("/auth/logout")
194|async def logout(response: Response, current_user: User = Depends(get_current_user)):
195|    # Delete session from database
196|    await db.sessions.delete_many({"user_id": current_user.id})
197|    
198|    # Clear cookie
199|    response.delete_cookie("session_token", path="/", secure=True, samesite="none")
200|    
201|    return {"message": "Logged out successfully"}
202|
203|@api_router.get("/auth/me", response_model=User)
204|async def get_current_user_info(current_user: User = Depends(get_current_user)):
205|    return current_user
206|
207|# User routes
208|@api_router.get("/users/{user_id}", response_model=User)
209|async def get_user(user_id: str):
210|    user = await db.users.find_one({"id": user_id})
211|    if not user:
212|        raise HTTPException(status_code=404, detail="User not found")
213|    return User(**user)
214|
215|@api_router.put("/users/me", response_model=User)
216|async def update_current_user(
217|    user_update: UserUpdate,
218|    current_user: User = Depends(get_current_user)
219|):
220|    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
221|    
222|    if update_data:
223|        await db.users.update_one(
224|            {"id": current_user.id},
225|            {"$set": update_data}
226|        )
227|    
228|    updated_user = await db.users.find_one({"id": current_user.id})
229|    return User(**updated_user)
230|
231|# Post routes
232|@api_router.post("/posts", response_model=Post)
233|async def create_post(
234|    post_data: PostCreate,
235|    current_user: User = Depends(get_current_user)
236|):
237|    post = Post(user_id=current_user.id, **post_data.dict())
238|    
239|    await db.posts.insert_one(post.dict())
240|    
241|    # Update user's posts count
242|    await db.users.update_one(
243|        {"id": current_user.id},
244|        {"$inc": {"posts_count": 1}}
245|    )
246|    
247|    return post
248|
249|@api_router.get("/posts", response_model=List[PostWithUser])
250|async def get_posts(
251|    limit: int = 20,
252|    offset: int = 0,
253|    current_user: User = Depends(get_current_user)
254|):
255|    # Get posts with user info
256|    pipeline = [
257|        {
258|            "$lookup": {
259|                "from": "users",
260|                "localField": "user_id",
261|                "foreignField": "id",
262|                "as": "user"
263|            }
264|        },
265|        {"$unwind": "$user"},
266|        {"$sort": {"created_at": -1}},
267|        {"$skip": offset},
268|        {"$limit": limit}
269|    ]
270|    
271|    posts_cursor = db.posts.aggregate(pipeline)
272|    posts = await posts_cursor.to_list(length=None)
273|    
274|    # Check which posts are liked by current user
275|    result = []
276|    for post in posts:
277|        like = await db.likes.find_one({
278|            "post_id": post["id"],
279|            "user_id": current_user.id
280|        })
281|        
282|        post_with_user = PostWithUser(
283|            id=post["id"],
284|            user_id=post["user_id"],
285|            user_name=post["user"]["name"],
286|            user_picture=post["user"].get("picture"),
287|            content=post["content"],
288|            image_url=post.get("image_url"),
289|            video_url=post.get("video_url"),
290|            build_category=post.get("build_category"),
291|            likes_count=post["likes_count"],
292|            comments_count=post["comments_count"],
293|            is_liked=bool(like),
294|            created_at=post["created_at"]
295|        )
296|        result.append(post_with_user)
297|    
298|    return result
299|
300|@api_router.get("/posts/{post_id}", response_model=PostWithUser)
301|async def get_post(post_id: str, current_user: User = Depends(get_current_user)):
302|    # Get post with user info
303|    pipeline = [
304|        {"$match": {"id": post_id}},
305|        {
306|            "$lookup": {
307|                "from": "users",
308|                "localField": "user_id",
309|                "foreignField": "id",
310|                "as": "user"
311|            }
312|        },
313|        {"$unwind": "$user"}
314|    ]
315|    
316|    posts_cursor = db.posts.aggregate(pipeline)
317|    posts = await posts_cursor.to_list(length=None)
318|    
319|    if not posts:
320|        raise HTTPException(status_code=404, detail="Post not found")
321|    
322|    post = posts[0]
323|    
324|    # Check if liked by current user
325|    like = await db.likes.find_one({
326|        "post_id": post_id,
327|        "user_id": current_user.id
328|    })
329|    
330|    return PostWithUser(
331|        id=post["id"],
332|        user_id=post["user_id"],
333|        user_name=post["user"]["name"],
334|        user_picture=post["user"].get("picture"),
335|        content=post["content"],
336|        image_url=post.get("image_url"),
337|        video_url=post.get("video_url"),
338|        build_category=post.get("build_category"),
339|        likes_count=post["likes_count"],
340|        comments_count=post["comments_count"],
341|        is_liked=bool(like),
342|        created_at=post["created_at"]
343|    )
344|
345|# Like routes
346|@api_router.post("/posts/{post_id}/like")
347|async def toggle_like(post_id: str, current_user: User = Depends(get_current_user)):
348|    # Check if already liked
349|    existing_like = await db.likes.find_one({
350|        "post_id": post_id,
351|        "user_id": current_user.id
352|    })
353|    
354|    if existing_like:
355|        # Unlike
356|        await db.likes.delete_one({"id": existing_like["id"]})
357|        await db.posts.update_one(
358|            {"id": post_id},
359|            {"$inc": {"likes_count": -1}}
360|        )
361|        return {"liked": False}
362|    else:
363|        # Like
364|        like = Like(post_id=post_id, user_id=current_user.id)
365|        await db.likes.insert_one(like.dict())
366|        await db.posts.update_one(
367|            {"id": post_id},
368|            {"$inc": {"likes_count": 1}}
369|        )
370|        return {"liked": True}
371|
372|# Comment routes
373|@api_router.post("/posts/{post_id}/comments", response_model=Comment)
374|async def create_comment(
375|    post_id: str,
376|    comment_data: CommentCreate,
377|    current_user: User = Depends(get_current_user)
378|):
379|    comment = Comment(
380|        post_id=post_id,
381|        user_id=current_user.id,
382|        **comment_data.dict()
383|    )
384|    
385|    await db.comments.insert_one(comment.dict())
386|    
387|    # Update post's comments count
388|    await db.posts.update_one(
389|        {"id": post_id},
390|        {"$inc": {"comments_count": 1}}
391|    )
392|    
393|    return comment
394|
395|@api_router.get("/posts/{post_id}/comments", response_model=List[Comment])
396|async def get_comments(post_id: str, limit: int = 50, offset: int = 0):
397|    comments = await db.comments.find(
398|        {"post_id": post_id}
399|    ).sort("created_at", -1).skip(offset).limit(limit).to_list(length=None)
400|    
401|    return [Comment(**comment) for comment in comments]
402|
403|# Follow routes
404|@api_router.post("/users/{user_id}/follow")
405|async def toggle_follow(user_id: str, current_user: User = Depends(get_current_user)):
406|    if user_id == current_user.id:
407|        raise HTTPException(status_code=400, detail="Cannot follow yourself")
408|    
409|    # Check if already following
410|    existing_follow = await db.follows.find_one({
411|        "follower_id": current_user.id,
412|        "following_id": user_id
413|    })
414|    
415|    if existing_follow:
416|        # Unfollow
417|        await db.follows.delete_one({"id": existing_follow["id"]})
418|        
419|        # Update counts
420|        await db.users.update_one(
421|            {"id": current_user.id},
422|            {"$inc": {"following_count": -1}}
423|        )
424|        await db.users.update_one(
425|            {"id": user_id},
426|            {"$inc": {"followers_count": -1}}
427|        )
428|        
429|        return {"following": False}
430|    else:
431|        # Follow
432|        follow = Follow(follower_id=current_user.id, following_id=user_id)
433|        await db.follows.insert_one(follow.dict())
434|        
435|        # Update counts
436|        await db.users.update_one(
437|            {"id": current_user.id},
438|            {"$inc": {"following_count": 1}}
439|        )
440|        await db.users.update_one(
441|            {"id": user_id},
442|            {"$inc": {"followers_count": 1}}
443|        )
444|        
445|        return {"following": True}
446|
447|@api_router.get("/users/{user_id}/posts", response_model=List[PostWithUser])
448|async def get_user_posts(
449|    user_id: str,
450|    limit: int = 20,
451|    offset: int = 0,
452|    current_user: User = Depends(get_current_user)
453|):
454|    # Get user's posts with user info
455|    pipeline = [
456|        {"$match": {"user_id": user_id}},
457|        {
458|            "$lookup": {
459|                "from": "users",
460|                "localField": "user_id",
461|                "foreignField": "id",
462|                "as": "user"
463|            }
464|        },
465|        {"$unwind": "$user"},
466|        {"$sort": {"created_at": -1}},
467|        {"$skip": offset},
468|        {"$limit": limit}
469|    ]
470|    
471|    posts_cursor = db.posts.aggregate(pipeline)
472|    posts = await posts_cursor.to_list(length=None)
473|    
474|    # Check which posts are liked by current user
475|    result = []
476|    for post in posts:
477|        like = await db.likes.find_one({
478|            "post_id": post["id"],
479|            "user_id": current_user.id
480|        })
481|        
482|        post_with_user = PostWithUser(
483|            id=post["id"],
484|            user_id=post["user_id"],
485|            user_name=post["user"]["name"],
486|            user_picture=post["user"].get("picture"),
487|            content=post["content"],
488|            image_url=post.get("image_url"),
489|            video_url=post.get("video_url"),
490|            build_category=post.get("build_category"),
491|            likes_count=post["likes_count"],
492|            comments_count=post["comments_count"],
493|            is_liked=bool(like),
494|            created_at=post["created_at"]
495|        )
496|        result.append(post_with_user)
497|    
498|    return result
499|
500|# Health check
501|@api_router.get("/")
502|async def root():
503|    return {"message": "CarCommunity API is running"}
504|
505|# Include the router in the main app
506|app.include_router(api_router)
507|
508|app.add_middleware(
509|    CORSMiddleware,
510|    allow_credentials=True,
511|    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
512|    allow_methods=["*"],
513|    allow_headers=["*"],
514|)
515|
516|# Configure logging
517|logging.basicConfig(
518|    level=logging.INFO,
519|    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
520|)
521|logger = logging.getLogger(__name__)
522|
523|@app.on_event("shutdown")
524|async def shutdown_db_client():
525|    client.close()
