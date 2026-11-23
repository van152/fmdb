bool __fastcall sub_1411919D0(_QWORD *a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  int v8; // ebp
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  int v15; // ebp
  __int64 v16; // rbx
  __int64 *v17; // r13
  __int64 v18; // r12
  unsigned __int64 v19; // rax
  unsigned __int64 v20; // r14
  unsigned __int64 v21; // rcx
  unsigned __int64 v22; // r14
  __int64 v23; // r15
  __int64 *v24; // rbx
  __int64 v25; // rbx
  __int64 v27; // rbx
  __int64 v28; // rbx
  __int64 v29; // rbx
  __int64 v30; // rax
  __int64 v31; // rbp
  unsigned __int64 i; // rbx
  _DWORD *v33; // rdi
  unsigned __int8 v34; // [rsp+2Dh] [rbp-7Bh] BYREF
  __int16 v35; // [rsp+2Eh] [rbp-7Ah] BYREF
  char v36[8]; // [rsp+30h] [rbp-78h] BYREF
  _QWORD *v37; // [rsp+38h] [rbp-70h]
  unsigned __int64 v38; // [rsp+40h] [rbp-68h]
  __int64 v39; // [rsp+48h] [rbp-60h] BYREF
  __int64 v40; // [rsp+50h] [rbp-58h]
  __int64 v41; // [rsp+58h] [rbp-50h]
  __int64 v42; // [rsp+60h] [rbp-48h]

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 9, a3: 4);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 10, a3: 4);
  if ( v5[4] != 0 )
    return false;
  if ( (unsigned __int16)qword_141B60330 >= 0xDDDu )
  {
    v6 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 11, a3: 4);
    if ( *(_DWORD *)(v6 + 16) != 0 )
      return false;
  }
  v7 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v7 + 8));
    (*(void (__fastcall **)(__int64, _QWORD *, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 13, a3: 4);
  }
  v8 = *(_DWORD *)(v7 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v7 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v7)(a1: v7, a2: 1);
  if ( v8 != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 108, a3: 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 14, a3: 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 126, a3: 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: (char *)a1 + 116, a2) == 0 )
    return false;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 127, a3: 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return false;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 124, a3: 2);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v35, a3: 2);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return false;
  v37 = a1 + 3;
  sub_140893BE0(a1: a1 + 3, a2: v35);
  if ( v35 > 0 )
  {
    v15 = 0;
    do
    {
      v16 = sub_141750CC0(a1: 48);
      *(_QWORD *)v16 = 0;
      *(_QWORD *)(v16 + 8) = 0;
      *(_QWORD *)(v16 + 16) = 0xFFFFFFFFLL;
      *(_QWORD *)(v16 + 24) = 0xFFFFFFFF00000000uLL;
      *(_QWORD *)(v16 + 32) = 0x76C0001076C0001LL;
      *(_WORD *)(v16 + 40) = 511;
      sub_141191E80(a1: v16, a2);
      v17 = (__int64 *)a1[4];
      if ( v17 == (__int64 *)a1[5] )
      {
        v18 = (__int64)v17 - a1[3];
        v19 = v18 >> 3;
        v20 = (unsigned __int64)(v18 >> 3) >> 1;
        v21 = 0x1FFFFFFFFFFFFFFFLL - v20;
        v22 = (v18 >> 3) + v20;
        v38 = (v18 >> 3) + 1;
        if ( v22 <= v38 )
          v22 = v19 + 1;
        if ( v19 > v21 )
          v22 = 0x1FFFFFFFFFFFFFFFLL;
        v23 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v22);
        *(_QWORD *)(v23 + v18) = v16;
        v24 = (__int64 *)a1[4];
        sub_141758A00(a1: v23, a2: a1[3], a3: (char *)v17 - a1[3]);
        if ( v24 != v17 )
          sub_141758A00(a1: v23 + v18 + 8, a2: v17, a3: a1[4] - (_QWORD)v17);
        if ( *v37 != 0 )
          sub_1407E4890(a1: qword_141ABD470, a2: *v37, a3: a1[5] - *v37);
        a1[3] = v23;
        a1[4] = v23 + 8 * v38;
        a1[5] = v23 + 8 * v22;
      }
      else
      {
        *v17 = v16;
        a1[4] += 8LL;
      }
      ++v15;
    }
    while ( (__int16)v15 < v35 );
  }
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return false;
  if ( (unsigned __int16)qword_141B60330 >= 0xDDDu )
  {
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 129, a3: 1);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return false;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 130, a3: 1);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return false;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 12, a3: 8);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return false;
    v30 = *a2;
    v39 = v30;
    if ( v30 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v30 + 8));
    if ( v39 != 0 )
    {
      (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v39 + 40LL))(a1: v39, a2: &v34, a3: 1);
      LOBYTE(v30) = v34;
      v40 = 0;
      v41 = 0;
      v42 = 0;
      if ( v34 == 0 )
        goto LABEL_46;
    }
    else
    {
      v42 = 0;
      v41 = 0;
      v40 = 0;
    }
    sub_141196590(a1: a1 + 6, a2: (unsigned __int8)v30, a3: v36);
    if ( v34 != 0 )
    {
      v31 = 0;
      for ( i = 0; i < v34; ++i )
      {
        sub_14156AF70(a1: v31 + a1[6], a2: &v39);
        v31 += 32;
      }
    }
LABEL_46:
    sub_1412E6FF0(a1: &v39);
    if ( (unsigned __int16)qword_141B60330 < 0xDDDu )
      return true;
    v33 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v33 + 40LL))(a1: v33, a2: (__int64)a1 + 131, a3: 1);
    return v33[4] == 0;
  }
  return true;
}
