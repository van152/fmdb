char __fastcall sub_143E6C5C0(_QWORD *a1, __int64 a2, __int64 a3, char a4, unsigned __int8 a5)
{
  _QWORD *v8; // r14
  __int64 v9; // rdx
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rax
  volatile signed __int32 *v13; // rcx
  __int64 v14; // rax
  volatile signed __int32 *v15; // rcx
  __int64 v16; // rax
  volatile signed __int32 *v17; // rcx
  __int64 v18; // rax
  volatile signed __int32 *v19; // rcx

  v8 = a1 + 8;
  if ( a4 != 0 )
  {
    sub_140F7EE40(a3, (_DWORD)v8, *(_QWORD *)(a3 + 152), a5, 1, 0);
    sub_140F7EE40(a3, (_DWORD)a1 + 72, *(_QWORD *)(a3 + 152), a5, 1, 0);
    sub_140F7EC80(a3, (_DWORD)a1 + 104, *(_QWORD *)(a3 + 24), a5, 1, 0);
  }
  else
  {
    a1[13] = 0;
    a1[9] = 0;
    *v8 = 0;
  }
  sub_140F7EC80(a3, (_DWORD)a1 + 80, *(_QWORD *)(a3 + 24), a5, 1, 0);
  sub_140F7FD40(a3, a1 + 11, a5);
  if ( a4 != 0 )
  {
    v10 = a1[8];
    if ( v10 == 0 || *(int *)(v10 + 8) < 0 || (v11 = a1[9]) == 0 || *(int *)(v11 + 8) < 0 )
    {
      v8[1] = 0;
      *v8 = 0;
      v12 = a1[3];
      v13 = (volatile signed __int32 *)(v12 - 4);
      if ( v12 != 0 && _InterlockedDecrement(v13) == 0 )
        sub_1412EC9A0(v13, v9);
      a1[3] = 0;
      v14 = a1[4];
      v15 = (volatile signed __int32 *)(v14 - 4);
      if ( v14 != 0 && _InterlockedDecrement(v15) == 0 )
        sub_1412EC9A0(v15, v9);
      a1[4] = 0;
      v16 = a1[6];
      v17 = (volatile signed __int32 *)(v16 - 4);
      if ( v16 != 0 && _InterlockedDecrement(v17) == 0 )
        sub_1412EC9A0(v17, v9);
      a1[6] = 0;
      v18 = a1[5];
      v19 = (volatile signed __int32 *)(v18 - 4);
      if ( v18 != 0 && _InterlockedDecrement(v19) == 0 )
        sub_1412EC9A0(v19, v9);
      a1[5] = 0;
    }
  }
  return 1;
}
