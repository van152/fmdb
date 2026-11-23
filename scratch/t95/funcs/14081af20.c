volatile signed __int32 **__fastcall sub_14081AF20(
        volatile signed __int32 *a1,
        volatile signed __int32 **a2,
        __int64 *a3,
        unsigned int a4,
        char a5,
        unsigned __int8 a6)
{
  __int64 v9; // rax
  __int64 v10; // rcx
  int **v11; // r13
  __int64 v12; // r15
  __int64 *v13; // rax
  __int64 *v14; // rdx
  __int64 *v15; // rcx
  __int64 *v16; // rsi
  _QWORD *v17; // rax
  __int64 v18; // rcx
  __int64 *v19; // rax
  __int64 *v20; // rdx
  __int64 *v21; // rcx
  __int64 *v22; // rsi
  volatile signed __int32 *v23; // rcx
  volatile signed __int32 *v24; // rsi
  volatile signed __int32 *v25; // rsi
  __int64 v26; // rcx
  __int64 v27; // rsi
  volatile signed __int32 *v28; // rcx
  int v29; // eax
  int v30; // ecx
  unsigned __int64 v31; // rcx
  volatile signed __int32 *v32; // rax
  __int64 v33; // rcx
  int v34; // eax
  volatile signed __int32 *v35; // rax
  volatile signed __int32 *v36; // rcx
  volatile signed __int32 *v37; // rcx
  __int64 v38; // rsi
  __int64 v39; // rdi
  volatile signed __int32 *v40; // rax
  volatile signed __int32 *v41; // rcx
  __int64 v42; // rcx
  unsigned __int64 v44; // [rsp+20h] [rbp-40h] BYREF
  volatile signed __int32 *v45; // [rsp+28h] [rbp-38h] BYREF
  int v46; // [rsp+38h] [rbp-28h]
  volatile signed __int32 *v47; // [rsp+40h] [rbp-20h] BYREF
  int v48; // [rsp+4Ch] [rbp-14h]
  volatile signed __int32 *v49; // [rsp+50h] [rbp-10h] BYREF
  _QWORD v50[9]; // [rsp+58h] [rbp-8h] BYREF

  v50[1] = -2;
  v50[0] = 0;
  if ( v50 != a3 )
  {
    v9 = *a3;
    if ( *a3 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v9 - 4));
    v50[0] = v9;
  }
  v11 = *(int ***)(*(__int64 (__fastcall **)(volatile signed __int32 *))(*(_QWORD *)a1 + 8LL))(a1);
  v12 = qword_141ABD468;
  if ( a5 != 0 && v50[0] != 0 && *(_DWORD *)v50[0] != 0 )
  {
    sub_140824C10(v10, &v44, v11, v50);
    v13 = *(__int64 **)(*(_QWORD *)(v12 + 8) + 16LL);
    v14 = (__int64 *)v13[1];
    v15 = v13;
    if ( *((_BYTE *)v14 + 25) == 0 )
    {
      v15 = *(__int64 **)(*(_QWORD *)(v12 + 8) + 16LL);
      do
      {
        v16 = v14 + 2;
        if ( v14[4] >= v44 )
        {
          v15 = v14;
          v16 = v14;
        }
        v14 = (__int64 *)*v16;
      }
      while ( *(_BYTE *)(*v16 + 25) == 0 );
    }
    if ( *((_BYTE *)v15 + 25) == 0 && v44 >= v15[4] && v15 != v13 )
    {
      v26 = v15[5];
      if ( v26 != 0 )
        goto LABEL_34;
    }
    v17 = (_QWORD *)(*(__int64 (__fastcall **)(volatile signed __int32 *))(*(_QWORD *)a1 + 16LL))(a1);
    sub_140824C10(v18, &v44, *v17, v50);
    v19 = *(__int64 **)(*(_QWORD *)(v12 + 8) + 16LL);
    v20 = (__int64 *)v19[1];
    v21 = v19;
    if ( *((_BYTE *)v20 + 25) == 0 )
    {
      v21 = *(__int64 **)(*(_QWORD *)(v12 + 8) + 16LL);
      do
      {
        v22 = v20 + 2;
        if ( v20[4] >= v44 )
        {
          v21 = v20;
          v22 = v20;
        }
        v20 = (__int64 *)*v22;
      }
      while ( *(_BYTE *)(*v22 + 25) == 0 );
    }
    if ( *((_BYTE *)v21 + 25) != 0 || v44 < v21[4] || v21 == v19 || (v26 = v21[5]) == 0 )
    {
      v23 = (volatile signed __int32 *)(v50[0] - 4LL);
      if ( v50[0] == 0 )
        v23 = nullptr;
      v24 = (volatile signed __int32 *)(qword_141B59EE0 - 4);
      if ( qword_141B59EE0 != 0 )
      {
        if ( v50[0] != 0 && _InterlockedDecrement(v23) == 0 )
          sub_1412EC9A0((__int64)v23);
        v50[0] = 0;
        _InterlockedIncrement(v24);
        v25 = v24 + 1;
      }
      else
      {
        if ( v50[0] != 0 && _InterlockedDecrement(v23) == 0 )
          sub_1412EC9A0((__int64)v23);
        v25 = nullptr;
      }
      v50[0] = v25;
    }
    else
    {
LABEL_34:
      _InterlockedIncrement((volatile signed __int32 *)(v26 + 8));
      if ( _InterlockedDecrement((volatile signed __int32 *)(v26 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v26)(v26, 1);
    }
  }
  v44 = 0;
  v27 = sub_1412EC810(264, 2);
  *(_QWORD *)v27 = 0x200000000LL;
  strcpy((char *)(v27 + 8), "[%");
  v28 = (volatile signed __int32 *)(v44 - 4);
  if ( v44 != 0 && _InterlockedDecrement(v28) == 0 )
    sub_1412EC9A0((__int64)v28);
  v44 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v27);
  v44 = v27 + 4;
  v29 = 0;
  v30 = 0;
  if ( *v11 != nullptr )
    v30 = **v11;
  if ( v50[0] != 0 )
  {
    v29 = *(_DWORD *)v50[0] + 1;
    if ( *(_DWORD *)v50[0] == 0 )
      v29 = 0;
  }
  sub_140805E00(&v47, &v44, (unsigned int)(v30 + v29 + 5));
  v31 = v44;
  if ( v44 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v44 - 4)) == 0 )
    sub_1412EC9A0(v31 - 4);
  sub_140806120(&v47, v11);
  sub_140807AB0(&v47, 2);
  v32 = v47;
  if ( v47 != nullptr )
  {
    v33 = v48;
    *(_WORD *)((char *)v47 + v48 + 8) = 12579;
    *((_BYTE *)v32 + v33 + 10) = 0;
    v48 += 2;
  }
  if ( v50[0] != 0 && *(_DWORD *)v50[0] != 0 )
  {
    sub_140807AB0(&v47, 1);
    if ( v47 != nullptr )
      *(_WORD *)((char *)v47 + v48++ + 8) = 45;
    sub_140806120(&v47, v50);
  }
  sub_140807AB0(&v47, 1);
  if ( v47 != nullptr && (*(_WORD *)((char *)v47 + v48 + 8) = 93, v34 = v48 + 1, ++v48, v47 != nullptr) )
  {
    *((_DWORD *)v47 + 1) = v34;
    v35 = v47;
    v49 = nullptr;
    if ( v47 != nullptr )
    {
      _InterlockedIncrement(v47);
      v49 = v35 + 1;
    }
  }
  else
  {
    v49 = nullptr;
  }
  sub_140824A20(v12, &v44, &v49);
  v36 = v49;
  if ( v49 != nullptr && _InterlockedDecrement(v49 - 1) == 0 )
    sub_1412EC9A0((__int64)(v36 - 1));
  v49 = a1;
  _InterlockedIncrement(a1 + 2);
  sub_14081D7C0(&v44, 1, &v49, a4);
  v37 = v49;
  if ( v49 != nullptr && _InterlockedDecrement(v49 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v37)(v37, 1);
  v38 = qword_141ABD468;
  *a2 = nullptr;
  if ( v46 == -1 || (v39 = *(_QWORD *)(*(_QWORD *)(v38 + 8) + 64LL), *(_QWORD *)(sub_140105F10() + 16) != v39) )
  {
    sub_14081DFC0(&v44, a6, 0xFFFFFFFFLL, &qword_141B59EE0);
    if ( *(_DWORD *)(*(_QWORD *)(v38 + 8) + 264LL) != 0 )
    {
      sub_14081EDF0(&v44, &v49);
      v40 = v49;
      if ( v49 == nullptr )
        goto LABEL_79;
      goto LABEL_78;
    }
    if ( &v45 != a2 )
    {
      v40 = v45;
      if ( v45 != nullptr )
      {
        *a2 = nullptr;
        _InterlockedIncrement(v40 - 1);
      }
LABEL_78:
      *a2 = v40;
    }
  }
LABEL_79:
  sub_14081D040(&v44);
  v41 = v47;
  if ( v47 != nullptr && _InterlockedDecrement(v47) == 0 )
    sub_1412EC9A0((__int64)v41);
  v42 = v50[0];
  if ( v50[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v50[0] - 4LL)) == 0 )
    sub_1412EC9A0(v42 - 4);
  return a2;
}
