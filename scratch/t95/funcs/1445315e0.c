char __fastcall sub_1445315E0(_DWORD *a1, int a2, __int64 *a3)
{
  __int64 *v5; // rbx
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rcx
  unsigned int v11; // eax
  __int64 v12; // rdx
  _DWORD *v13; // rcx
  __int64 v14; // rax
  _DWORD *v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rax
  __int64 v18; // rcx
  int v19; // xmm6_4
  __int64 v20; // rax
  __int64 v21; // rax
  __int64 v22; // rcx
  _DWORD *v24; // [rsp+20h] [rbp-30h] BYREF
  __int64 v25; // [rsp+28h] [rbp-28h] BYREF
  _QWORD v26[2]; // [rsp+30h] [rbp-20h] BYREF

  v26[1] = -2;
  if ( a2 == 1130723442 )
  {
    v19 = a1[14];
    v20 = sub_14083D4F0(a1) + 104;
    LODWORD(v26[0]) = v19;
    v25 = v20;
    if ( &v25 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v21 = v25;
      v22 = v26[0];
      a3[1] = v26[0];
      *a3 = v21;
      v20 = sub_14083D4F0(v22) + 8;
      v26[0] = 0;
      v25 = v20;
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, &v25);
    return 1;
  }
  if ( a2 == 1684172397 || a2 == 1131307373 )
  {
    v5 = (__int64 *)(a1 + 6);
    v6 = sub_14083D4F0(a1);
    v26[0] = 0;
    if ( v26 != v5 )
    {
      v7 = *v5;
      if ( *v5 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v7 - 4));
      v26[0] = v7;
    }
    v8 = v6 + 136;
    v25 = v8;
    if ( &v25 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v9 = v25;
      v10 = v26[0];
      a3[1] = v26[0];
      *a3 = v9;
      v8 = sub_14083D4F0(v10) + 8;
      v26[0] = 0;
      v25 = v8;
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v8 + 16LL))(v8, &v25);
    v11 = sub_14157FD30((unsigned int)a1[3]);
    if ( (_BYTE)v11 != 0xFF )
    {
      v24 = nullptr;
      sub_140DA2220(&v24, v11);
      v13 = v24;
      if ( v24 != nullptr )
      {
        if ( *v24 == 0 )
          goto LABEL_18;
        v14 = sub_14083D4F0(v24);
        v26[0] = 0;
        v15 = v24;
        if ( v24 != nullptr )
          _InterlockedIncrement(v24 - 1);
        v26[0] = v15;
        v16 = v14 + 136;
        v25 = v16;
        if ( &v25 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v17 = v25;
          v18 = v26[0];
          a3[1] = v26[0];
          *a3 = v17;
          v16 = sub_14083D4F0(v18) + 8;
          v26[0] = 0;
          v25 = v16;
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, &v25);
        v13 = v24;
        if ( v24 != nullptr )
        {
LABEL_18:
          if ( _InterlockedDecrement(v13 - 1) == 0 )
            sub_1412EC9A0(v13 - 1, v12);
        }
      }
    }
    return 1;
  }
  return sub_140FE3F20(a1, a2, a3);
}
