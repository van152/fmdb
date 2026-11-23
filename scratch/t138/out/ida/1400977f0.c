__int64 __fastcall sub_1400977F0(__int64 a1, __int64 a2, _QWORD **a3, __int64 a4)
{
  __int64 v7; // rbp
  __int64 v8; // rsi
  __int64 *v9; // rbp
  _QWORD *v10; // r15
  unsigned __int64 v11; // rsi
  volatile signed __int32 *v12; // r14
  volatile signed __int32 *v13; // rcx
  __int64 *v14; // rcx
  __int64 *v15; // rax
  _QWORD *v16; // rcx
  void (__fastcall ***v17)(_QWORD, __int64); // rcx
  void (__fastcall ***v18)(_QWORD, __int64); // rcx
  void (__fastcall ***v19)(_QWORD, __int64); // rcx
  void (__fastcall ***v20)(_QWORD, __int64); // rcx
  volatile signed __int32 *v22; // [rsp+40h] [rbp-78h] BYREF
  __int64 v23; // [rsp+48h] [rbp-70h] BYREF
  __int64 v24; // [rsp+50h] [rbp-68h] BYREF
  __int64 v25; // [rsp+58h] [rbp-60h] BYREF
  __int64 v26; // [rsp+60h] [rbp-58h] BYREF
  int v27; // [rsp+68h] [rbp-50h] BYREF
  _BYTE v28[72]; // [rsp+70h] [rbp-48h] BYREF

  sub_1407D5DC0(a1: qword_141ABD878, a2: &v26, a3: &qword_141B5ACC0);
  v7 = v26;
  if ( v26 == 0 )
  {
    LODWORD(v9) = 0;
    return (unsigned int)v9;
  }
  sub_1407D5F40(a1: &v24, a2: a4);
  sub_1407D2430(a1: v7, a2: &v25, a3: &v24);
  sub_140808B00(a1: &v24);
  if ( v25 == 0 )
  {
    LODWORD(v9) = 0;
    goto LABEL_36;
  }
  v8 = qword_141ABF5C0;
  v9 = &v24;
  sub_1407D8AB0(a1: &v24, a2: 0x1418E2C24LL);
  sub_1407D5F40(a1: &v23, a2);
  sub_1400015E0(a1: v8, a2: &v25, a3: &v23, a4: &v24, a5: 1);
  sub_140808B00(a1: &v23);
  sub_1407D8AB0(a1: &v23, a2: 0x1418E2C24LL);
  sub_1407D5F40(a1: &v22, a2);
  sub_1407D1400(
    a1: (unsigned int)&v24,
    a2: (unsigned int)&v25,
    a3: (unsigned int)&v22,
    a4: (unsigned int)&v23,
    a5: 1,
    a6: 0);
  sub_140808B00(a1: &v22);
  if ( v24 == 0 )
  {
    LODWORD(v9) = 0;
    goto LABEL_33;
  }
  sub_1407D5F40(a1: &v22, a2);
  sub_1407C7270(
    a1: (unsigned int)&v23,
    a2: (unsigned int)&v24,
    a3: (unsigned int)&v25,
    a4: (unsigned int)&v22,
    a5: 3,
    a6: 0,
    a7: 2);
  sub_140808B00(a1: &v22);
  if ( v23 == 0 )
  {
    LODWORD(v9) = 0;
    goto LABEL_30;
  }
  v10 = (_QWORD *)**a3;
  LOBYTE(v9) = 1;
  if ( v10 == *a3 )
    goto LABEL_27;
  while ( 1 )
  {
    sub_1407D8AB0(a1: &v27, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v28, a2: v10 + 4);
    sub_1407D1400(
      a1: (unsigned int)&v22,
      a2: (unsigned int)&v23,
      a3: (unsigned int)v28,
      a4: (unsigned int)&v27,
      a5: 1,
      a6: 0);
    sub_140808B00(a1: v28);
    if ( v22 != nullptr )
      break;
LABEL_13:
    v14 = (__int64 *)v10[2];
    if ( *((_BYTE *)v14 + 25) != 0 )
    {
      do
      {
        v15 = (__int64 *)v10[1];
        if ( *((_BYTE *)v15 + 25) != 0 )
          break;
        v16 = v10;
        v10 = (_QWORD *)v10[1];
      }
      while ( v16 == (_QWORD *)v15[2] );
    }
    else
    {
      do
      {
        v15 = v14;
        v14 = (__int64 *)*v14;
      }
      while ( *((_BYTE *)v14 + 25) == 0 );
    }
    v10 = v15;
    if ( v15 == *a3 )
      goto LABEL_27;
  }
  v11 = v10[6] - v10[5];
  v27 = v11 >> 2;
  (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v22 + 40LL))(a1: v22, a2: &v27, a3: 4);
  v12 = v22;
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD, unsigned __int64))(*(_QWORD *)v22 + 40LL))(
    a1: v22,
    a2: v10[5],
    a3: v11);
  v13 = v22;
  if ( *((_DWORD *)v12 + 4) == 0 )
  {
    if ( v22 != nullptr && _InterlockedDecrement(v22 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v13)(a1: v13, a2: 1);
    goto LABEL_13;
  }
  if ( v22 != nullptr && _InterlockedDecrement(v22 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v13)(a1: v13, a2: 1);
  LODWORD(v9) = 0;
LABEL_27:
  v17 = (void (__fastcall ***)(_QWORD, __int64))v23;
  if ( v23 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 + 8)) == 0 )
    (**v17)(a1: v17, a2: 1);
LABEL_30:
  v18 = (void (__fastcall ***)(_QWORD, __int64))v24;
  if ( v24 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 8)) == 0 )
    (**v18)(a1: v18, a2: 1);
LABEL_33:
  v19 = (void (__fastcall ***)(_QWORD, __int64))v25;
  if ( v25 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25 + 8)) == 0 )
    (**v19)(a1: v19, a2: 1);
LABEL_36:
  v20 = (void (__fastcall ***)(_QWORD, __int64))v26;
  if ( v26 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 + 8)) == 0 )
    (**v20)(a1: v20, a2: 1);
  return (unsigned int)v9;
}
