char __fastcall sub_143E54890(__int64 a1, int a2, __int64 *a3)
{
  __int64 **v3; // r11
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 **v6; // r10
  __int64 **v7; // r9
  char *v8; // r10
  unsigned __int64 v9; // rcx
  __int64 *v10; // rsi
  __int64 v11; // rdx
  volatile signed __int32 *v12; // rcx
  volatile signed __int32 *v13; // rdi
  volatile signed __int32 *v14; // rdi
  __int64 v15; // rcx
  __int64 v16; // rsi

  v3 = *(__int64 ***)(a1 + 152);
  v4 = *(_QWORD *)(a1 + 160) - (_QWORD)v3;
  if ( v4 < 8 )
    return v4;
  v4 = (unsigned __int64)v4 >> 3;
  v5 = v4;
  while ( 1 )
  {
    v5 = (unsigned __int64)v5 >> 1;
    v6 = &v3[v5];
    if ( *((_DWORD *)*v6 + 4) >= a2 )
      break;
    v5 = v4 + ~v5;
    v3 = v6 + 1;
LABEL_5:
    v4 = v5;
    if ( v5 <= 0 )
      return v4;
  }
  if ( *((_DWORD *)*v6 + 4) > a2 )
    goto LABEL_5;
  v7 = v3;
  if ( (unsigned __int64)v4 >= 2 )
  {
    v15 = v5 & 0x1FFFFFFFFFFFFFFFLL;
    v7 = v3;
    v16 = v15;
    do
    {
      v16 = (unsigned __int64)v16 >> 1;
      if ( *((_DWORD *)v7[v16] + 4) < a2 )
      {
        v7 += v16 + 1;
        v16 = v15 + ~v16;
      }
      v15 = v16;
    }
    while ( v16 > 0 );
  }
  v8 = (char *)(v6 + 1);
  if ( (char *)&v3[v4] - v8 > 0 )
  {
    v9 = (unsigned __int64)((char *)&v3[v4] - v8) >> 3;
    v4 = v9;
    do
    {
      v4 = (unsigned __int64)v4 >> 1;
      if ( *(_DWORD *)(*(_QWORD *)&v8[8 * v4] + 16LL) <= a2 )
      {
        v8 += 8 * v4 + 8;
        v4 = v9 + ~v4;
      }
      v9 = v4;
    }
    while ( v4 > 0 );
  }
  if ( v7 != (__int64 **)v8 )
  {
    v10 = *v7;
    if ( *v7 != a3 )
    {
      v11 = *a3;
      v4 = *v10;
      v12 = (volatile signed __int32 *)(*v10 - 4);
      if ( *v10 == 0 )
        v12 = nullptr;
      v13 = (volatile signed __int32 *)(v11 - 4);
      if ( v11 != 0 )
      {
        if ( v4 != 0 && _InterlockedDecrement(v12) == 0 )
          LOBYTE(v4) = sub_1412EC9A0((__int64)v12);
        *v10 = 0;
        _InterlockedIncrement(v13);
        v14 = v13 + 1;
      }
      else
      {
        if ( v4 != 0 && _InterlockedDecrement(v12) == 0 )
          LOBYTE(v4) = sub_1412EC9A0((__int64)v12);
        v14 = nullptr;
      }
      *v10 = (__int64)v14;
    }
  }
  return v4;
}
