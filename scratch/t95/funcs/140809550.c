volatile signed __int32 **__fastcall sub_140809550(
        volatile signed __int32 **a1,
        volatile signed __int32 **a2,
        unsigned int **a3)
{
  volatile signed __int32 **v3; // rax
  volatile signed __int32 *v5; // rdx
  unsigned int *v6; // rax
  __int64 v7; // rdx
  volatile signed __int32 *v8; // rax
  volatile signed __int32 *v9; // rdx
  volatile signed __int32 *v10; // rcx
  volatile signed __int32 *v11; // rsi
  volatile signed __int32 *v12; // rsi

  v3 = (volatile signed __int32 **)a3;
  *a2 = nullptr;
  LOBYTE(a3) = 1;
  if ( a2 == a1 )
  {
    v5 = nullptr;
  }
  else
  {
    v5 = *a1;
    if ( *a1 == nullptr )
    {
      v5 = nullptr;
      if ( a2 == v3 )
        return a2;
      goto LABEL_13;
    }
    _InterlockedIncrement(v5 - 1);
    *a2 = v5;
    a3 = nullptr;
    if ( *v5 != 0 )
    {
      v6 = (unsigned int *)*v3;
      if ( v6 != nullptr )
        a3 = (unsigned int **)*v6;
      v7 = 0x1419435F1LL;
      if ( v6 != nullptr )
        v7 = (__int64)(v6 + 1);
      sub_140809710(a2, v7, a3);
      return a2;
    }
  }
  if ( a2 == v3 )
    return a2;
LABEL_13:
  v8 = *v3;
  v9 = v5 - 1;
  v10 = nullptr;
  if ( (_BYTE)a3 == 0 )
    v10 = v9;
  v11 = v8 - 1;
  if ( v8 != nullptr )
  {
    if ( (_BYTE)a3 == 0 && _InterlockedDecrement(v10) == 0 )
      sub_1412EC9A0((__int64)v10);
    *a2 = nullptr;
    _InterlockedIncrement(v11);
    v12 = v11 + 1;
  }
  else
  {
    if ( (_BYTE)a3 == 0 && _InterlockedDecrement(v10) == 0 )
      sub_1412EC9A0((__int64)v10);
    v12 = nullptr;
  }
  *a2 = v12;
  return a2;
}
