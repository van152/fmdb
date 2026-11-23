__int64 __fastcall sub_140F10660(_QWORD *a1)
{
  __int64 *v2; // rax
  __int64 *v3; // rdx
  __int64 *v4; // rcx
  __int64 *v5; // rbx
  __int64 *v6; // rdi
  __int64 v7; // rbx
  __int64 v8; // rdi
  __int64 v9; // rcx
  __int64 *v10; // rdi
  __int64 v11; // rbx
  __int64 v12; // rdi
  __int64 v13; // rcx
  __int64 *v14; // rax
  __int64 *v15; // rdx
  __int64 *v16; // rcx
  __int64 *v17; // rbx
  __int64 *v18; // rdi
  _QWORD *v19; // rax
  __int64 v20; // rax
  __int64 v21; // rax
  __int64 v22; // rax
  __int64 v23; // rbx
  int v24; // ebp
  __int64 v25; // rdi
  __int64 v26; // rcx
  __int64 *v27; // rdi
  __int64 result; // rax
  __int64 v29; // rbx
  int v30; // ebp
  __int64 v31; // rdi
  __int64 v32; // rcx
  __int64 (__fastcall ***v33)(_QWORD, __int64); // rcx
  __int64 (__fastcall ***v34)(_QWORD, __int64); // rcx
  __int64 v35; // rsi
  __int64 v36; // rcx
  __int64 v37; // rsi
  __int64 v38; // rcx
  __int64 v39; // [rsp+38h] [rbp-70h] BYREF
  __int64 v40; // [rsp+40h] [rbp-68h] BYREF
  __int64 v41; // [rsp+48h] [rbp-60h] BYREF
  char v42[8]; // [rsp+50h] [rbp-58h] BYREF
  __int64 v43; // [rsp+58h] [rbp-50h] BYREF
  __int64 v44[9]; // [rsp+60h] [rbp-48h] BYREF

  v2 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v3 = (__int64 *)v2[1];
  v4 = v2;
  if ( *((_BYTE *)v3 + 25) == 0 )
  {
    v4 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v5 = v3 + 2;
      if ( v3[4] >= (unsigned __int64)qword_141B5EDF0 )
      {
        v4 = v3;
        v5 = v3;
      }
      v3 = (__int64 *)*v5;
    }
    while ( *(_BYTE *)(*v5 + 25) == 0 );
  }
  if ( *((_BYTE *)v4 + 25) != 0 || qword_141B5EDF0 < (unsigned __int64)v4[4] || v4 == v2 )
  {
    v41 = 0;
  }
  else
  {
    v20 = v4[5];
    v41 = v20;
    if ( v20 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v20 + 8));
  }
  v6 = (__int64 *)a1[141];
  if ( v6 == nullptr )
    goto LABEL_12;
  if ( *((_WORD *)v6 + 81) != 0 || v6[8] != 0 )
  {
    sub_140FB5070(a1: a1[141]);
    sub_141750CFC(a1: v6);
LABEL_12:
    v7 = sub_141750CC0(a1: 168);
    sub_14080D0E0(a1: v44, a2: 0x1418E2C24LL);
    v8 = sub_1412EC810(a1: 264, a2: 7);
    *(_QWORD *)v8 = 0x700000000LL;
    strcpy((char *)(v8 + 8), "pl_hist");
    _InterlockedIncrement((volatile signed __int32 *)v8);
    v39 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v8);
    v39 = v8 + 4;
    sub_14120E200(a1: v7, a2: (unsigned int)&v41, a3: (unsigned int)&v39, a4: v44[0], a5: 3, a6: 0, a7: 40);
    a1[141] = v7;
    v9 = v39;
    if ( v39 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 - 4)) == 0 )
      sub_1412EC9A0(a1: v9 - 4);
    if ( _InterlockedDecrement((volatile signed __int32 *)v8) == 0 )
      sub_1412EC9A0(a1: v8);
    goto LABEL_17;
  }
  v35 = v41;
  v36 = *v6;
  if ( *v6 != v41 )
  {
    if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v36)(a1: v36, a2: 1);
    *v6 = v41;
    if ( v35 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v35 + 8));
  }
LABEL_17:
  v10 = (__int64 *)a1[143];
  if ( v10 == nullptr )
    goto LABEL_21;
  if ( *((_WORD *)v10 + 81) != 0 || v10[8] != 0 )
  {
    sub_140FB5070(a1: a1[143]);
    sub_141750CFC(a1: v10);
LABEL_21:
    v11 = sub_141750CC0(a1: 168);
    sub_14080D0E0(a1: &v43, a2: 0x1418E2C24LL);
    v12 = sub_1412EC810(a1: 264, a2: 11);
    *(_QWORD *)v12 = 0xB00000000LL;
    strcpy((char *)(v12 + 8), "non_pl_hist");
    _InterlockedIncrement((volatile signed __int32 *)v12);
    v39 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v12);
    v39 = v12 + 4;
    sub_14120E200(a1: v11, a2: (unsigned int)&v41, a3: (unsigned int)&v39, a4: v43, a5: 3, a6: 0, a7: 20);
    a1[143] = v11;
    v13 = v39;
    if ( v39 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 - 4)) == 0 )
      sub_1412EC9A0(a1: v13 - 4);
    if ( _InterlockedDecrement((volatile signed __int32 *)v12) == 0 )
      sub_1412EC9A0(a1: v12);
    goto LABEL_26;
  }
  v37 = v41;
  v38 = *v10;
  if ( *v10 != v41 )
  {
    if ( v38 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v38)(a1: v38, a2: 1);
    *v10 = v37;
    if ( v37 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v37 + 8));
  }
LABEL_26:
  v14 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v15 = (__int64 *)v14[1];
  v16 = v14;
  if ( *((_BYTE *)v15 + 25) == 0 )
  {
    v16 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v17 = v15 + 2;
      if ( v15[4] >= (unsigned __int64)qword_141B59838 )
      {
        v16 = v15;
        v17 = v15;
      }
      v15 = (__int64 *)*v17;
    }
    while ( *(_BYTE *)(*v17 + 25) == 0 );
  }
  if ( *((_BYTE *)v16 + 25) != 0 || qword_141B59838 < (unsigned __int64)v16[4] || v16 == v14 )
  {
    v39 = 0;
  }
  else
  {
    v21 = v16[5];
    v39 = v21;
    if ( v21 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v21 + 8));
  }
  v18 = (__int64 *)a1[142];
  if ( v18 != nullptr )
  {
    v19 = (_QWORD *)v18[1];
    if ( v19 != nullptr )
    {
      if ( *v19 == v19[1] )
        goto LABEL_54;
    }
    else
    {
      v22 = *v18;
      if ( *v18 == 0 || *(_WORD *)(v22 + 162) == 0 && *(_QWORD *)(v22 + 64) == 0 )
        goto LABEL_54;
    }
    sub_140EFF130(a1: a1[142]);
    sub_141750CFC(a1: v18);
  }
  v23 = sub_141750CC0(a1: 24);
  v24 = sub_1400870E0();
  sub_14080D0E0(a1: v42, a2: 0x1418DF862LL);
  v25 = sub_1412EC810(a1: 264, a2: 7);
  *(_QWORD *)v25 = 0x700000000LL;
  strcpy((char *)(v25 + 8), "pl_hist");
  _InterlockedIncrement((volatile signed __int32 *)v25);
  v40 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v25);
  v40 = v25 + 4;
  sub_140F20860(a1: v23, a2: (unsigned int)&v39, a3: (unsigned int)&v40, a4: (unsigned int)v42, a5: v24);
  a1[142] = v23;
  v26 = v40;
  if ( v40 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v40 - 4)) == 0 )
    sub_1412EC9A0(a1: v26 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v25) == 0 )
    sub_1412EC9A0(a1: v25);
LABEL_54:
  v27 = (__int64 *)a1[144];
  if ( v27 != nullptr )
  {
    result = v27[1];
    if ( result != 0 )
    {
      if ( *(_QWORD *)result == *(_QWORD *)(result + 8) )
        goto LABEL_67;
    }
    else
    {
      result = *v27;
      if ( *v27 == 0 )
        goto LABEL_67;
      if ( *(_WORD *)(result + 162) == 0 )
      {
        result += 64;
        if ( *(_QWORD *)result == 0 )
          goto LABEL_67;
      }
    }
    sub_140EFF3E0(a1: a1[144]);
    sub_141750CFC(a1: v27);
  }
  v29 = sub_141750CC0(a1: 24);
  v30 = sub_1400870E0();
  sub_14080D0E0(a1: v42, a2: 0x1418DF862LL);
  v31 = sub_1412EC810(a1: 264, a2: 11);
  *(_QWORD *)v31 = 0xB00000000LL;
  strcpy((char *)(v31 + 8), "non_pl_hist");
  _InterlockedIncrement((volatile signed __int32 *)v31);
  v40 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v31);
  v40 = v31 + 4;
  result = sub_140F20F70(a1: v29, a2: (unsigned int)&v39, a3: (unsigned int)&v40, a4: (unsigned int)v42, a5: v30);
  a1[144] = v29;
  v32 = v40;
  if ( v40 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v40 - 4)) == 0 )
    result = sub_1412EC9A0(a1: v32 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v31) == 0 )
    result = sub_1412EC9A0(a1: v31);
LABEL_67:
  v33 = (__int64 (__fastcall ***)(_QWORD, __int64))v39;
  if ( v39 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 + 8)) == 0 )
    result = (**v33)(a1: v33, a2: 1);
  v34 = (__int64 (__fastcall ***)(_QWORD, __int64))v41;
  if ( v41 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v41 + 8)) == 0 )
    return (**v34)(a1: v34, a2: 1);
  return result;
}
