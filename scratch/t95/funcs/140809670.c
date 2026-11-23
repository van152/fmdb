volatile signed __int32 **__fastcall sub_140809670(volatile signed __int32 **a1, unsigned int **a2)
{
  volatile signed __int32 *v3; // rax
  unsigned int *v4; // rax
  __int64 v5; // r8
  unsigned int *v6; // rdx
  volatile signed __int32 *v7; // rcx
  volatile signed __int32 *v8; // rdi
  volatile signed __int32 *v9; // rdi
  __int64 v10; // rdx

  v3 = *a1;
  if ( *a1 != nullptr && *v3 != 0 )
  {
    v4 = *a2;
    if ( *a2 != nullptr )
      v5 = *v4;
    else
      v5 = 0;
    v10 = 0x1419435F1LL;
    if ( v4 != nullptr )
      v10 = (__int64)(v4 + 1);
    sub_140809710(a1, v10, v5);
  }
  else if ( a1 != (volatile signed __int32 **)a2 )
  {
    v6 = *a2;
    v7 = v3 - 1;
    if ( v3 == nullptr )
      v7 = nullptr;
    v8 = (volatile signed __int32 *)(v6 - 1);
    if ( v6 != nullptr )
    {
      if ( v3 != nullptr && _InterlockedDecrement(v7) == 0 )
        sub_1412EC9A0((__int64)v7);
      *a1 = nullptr;
      _InterlockedIncrement(v8);
      v9 = v8 + 1;
    }
    else
    {
      if ( v3 != nullptr && _InterlockedDecrement(v7) == 0 )
        sub_1412EC9A0((__int64)v7);
      v9 = nullptr;
    }
    *a1 = v9;
  }
  return a1;
}
