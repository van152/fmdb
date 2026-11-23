// THUNK ALIAS -> sub_1444C8000 (jmp:0x1415322b0->0x1444c8000)
_QWORD *__fastcall sub_1444C8000(__int64 a1, _QWORD *a2)
{
  volatile signed __int32 *v4; // rbx
  volatile signed __int32 *v5; // rdx
  unsigned int v6; // esi
  __int64 *v7; // rax
  __int64 v8; // rsi
  int v9; // ecx
  __int64 v10; // rax
  int *v11; // rdx
  __int64 v12; // rax
  volatile signed __int32 *v13; // rax
  volatile signed __int32 *v14; // rcx
  volatile signed __int32 *v16[2]; // [rsp+20h] [rbp-20h] BYREF
  __int64 v17; // [rsp+38h] [rbp-8h]

  v17 = -2;
  *(_OWORD *)v16 = 0;
  v4 = (volatile signed __int32 *)sub_1412EC810(264, 1024);
  *(_QWORD *)v4 = 0x40000000000LL;
  *((_BYTE *)v4 + 8) = 0;
  v5 = v16[0];
  if ( v16[0] == nullptr )
  {
LABEL_10:
    LODWORD(v16[1]) = 0;
    _InterlockedIncrement(v4);
    v16[0] = v4;
    LODWORD(v16[1]) = *((_DWORD *)v4 + 1);
    goto LABEL_11;
  }
  v6 = 1024;
  if ( SHIDWORD(v16[1]) < 1024 )
    v6 = HIDWORD(v16[1]);
  if ( SHIDWORD(v16[1]) > 0 )
  {
    sub_141758A00();
    *((_BYTE *)v4 + v6 + 8) = 0;
    v5 = v16[0];
  }
  HIDWORD(v16[1]) = v6;
  if ( v5 != v4 )
  {
    if ( v5 != nullptr && _InterlockedDecrement(v5) == 0 )
      sub_1412EC9A0((__int64)v5);
    goto LABEL_10;
  }
LABEL_11:
  v7 = *(__int64 **)(*(_QWORD *)a1 + 312LL);
  if ( v7 == nullptr )
    goto LABEL_20;
  v8 = 0;
  do
  {
    v9 = *((_DWORD *)v7 + 2);
    v10 = *v7;
    if ( v8 >= (char)((unsigned int)(v9 - v10) >> 3) )
      break;
    v11 = *(int **)(v10 + 8 * v8);
    if ( *v11 != -1 )
    {
      v12 = sub_140F7A940(qword_141B5FDC0, v11);
      if ( v12 != 0 )
      {
        sub_140806120(v16, v12 + 64);
        sub_140807AB0(v16, 1);
        if ( v16[0] != nullptr )
        {
          *(_WORD *)((char *)v16[0] + SHIDWORD(v16[1]) + 8) = 32;
          ++HIDWORD(v16[1]);
        }
      }
    }
    ++v8;
    v7 = *(__int64 **)(*(_QWORD *)a1 + 312LL);
  }
  while ( v7 != nullptr );
  v4 = v16[0];
  if ( v16[0] == nullptr )
  {
    *a2 = 0;
  }
  else
  {
LABEL_20:
    *((_DWORD *)v4 + 1) = HIDWORD(v16[1]);
    v13 = v16[0];
    *a2 = 0;
    if ( v13 != nullptr )
    {
      _InterlockedIncrement(v13);
      *a2 = v13 + 1;
      v14 = v16[0];
      if ( v16[0] != nullptr && _InterlockedDecrement(v16[0]) == 0 )
        sub_1412EC9A0((__int64)v14);
    }
  }
  return a2;
}
