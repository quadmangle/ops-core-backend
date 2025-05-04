from app.security import set_rls_context

@router.get("/me")
async def get_my_user(request: Request):
    await set_rls_context(request)
    # now any query respects RLS automatically
    return {"user_id": request.state.user_id}
