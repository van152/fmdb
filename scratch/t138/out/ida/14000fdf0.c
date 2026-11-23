unsigned __int64 __fastcall sub_14000FDF0(_QWORD *a1)
{
  unsigned __int64 result; // rax
  _QWORD *v3; // r15
  _QWORD *v4; // rsi
  _QWORD *v5; // rbx
  _QWORD *v6; // rdi
  __int64 v7; // rbp
  __int64 v8; // rbp
  __int64 (__fastcall ***v9)(_QWORD, __int64); // rcx
  __int64 v10; // rdi
  __int64 v11; // rdi
  _QWORD *v12; // r12
  unsigned __int64 v13; // rbp
  volatile signed __int32 *v14; // rdi
  volatile signed __int32 *v15; // rdi
  _QWORD *v16; // rsi
  __int64 v17; // rax
  _QWORD *v18; // r15
  int v19; // edi
  __int64 (__fastcall ***v20)(_QWORD, __int64); // rcx
  volatile signed __int32 *v21; // rcx
  volatile signed __int32 *v22; // rdi
  volatile signed __int32 *v23; // rdi
  volatile signed __int32 *v24; // rcx
  volatile signed __int32 *v25; // rcx
  volatile signed __int32 *v26; // rcx
  volatile signed __int32 *v27; // rsi
  __int64 (__fastcall ***v28)(_QWORD, __int64); // rcx
  __int64 (__fastcall ***v29)(_QWORD, __int64); // rcx
  __int64 (__fastcall ***v30)(_QWORD, __int64); // rcx
  char v31; // [rsp+47h] [rbp-101h] BYREF
  volatile signed __int32 *v32; // [rsp+48h] [rbp-100h] BYREF
  char v33[8]; // [rsp+50h] [rbp-F8h] BYREF
  volatile signed __int32 *v34; // [rsp+58h] [rbp-F0h] BYREF
  __int64 v35; // [rsp+60h] [rbp-E8h] BYREF
  volatile signed __int32 *v36; // [rsp+68h] [rbp-E0h] BYREF
  __int64 v37; // [rsp+70h] [rbp-D8h] BYREF
  _DWORD v38[4]; // [rsp+78h] [rbp-D0h] BYREF
  _BYTE v39[4]; // [rsp+88h] [rbp-C0h] BYREF
  unsigned __int16 v40; // [rsp+8Ch] [rbp-BCh]
  unsigned __int64 v41; // [rsp+90h] [rbp-B8h] BYREF
  _QWORD *v42; // [rsp+98h] [rbp-B0h]
  _QWORD v43[3]; // [rsp+A0h] [rbp-A8h] BYREF
  _DWORD v44[4]; // [rsp+B8h] [rbp-90h] BYREF
  _QWORD v45[16]; // [rsp+C8h] [rbp-80h] BYREF

  v37 = 0;
  result = sub_14000F1D0(a1: &v37);
  if ( (_BYTE)result == 0 )
    goto LABEL_61;
  v3 = a1 + 56;
  sub_140AFEBC0(a1: a1 + 56);
  v4 = (_QWORD *)a1[5553];
  v5 = (_QWORD *)a1[5554];
  if ( v4 != v5 )
  {
    v6 = (_QWORD *)a1[5553];
    do
    {
      v7 = *v6;
      if ( *v6 != 0 )
      {
        sub_14083D320(a1: *v6);
        sub_1400039E0(a1: v7);
      }
      ++v6;
    }
    while ( v6 != v5 );
    v8 = a1[5554] - (_QWORD)v5;
    sub_141758A00(a1: v4, a2: v5, a3: v8);
    a1[5554] = (char *)v4 + v8;
  }
  sub_140053610(a1: a1 + 5559, a2: v45, a3: a1[5559], a4: a1[5560]);
  sub_1407D8AB0(a1: v45, a2: 0x14191EB1BLL);
  sub_1407D1120(
    a1: (unsigned int)&v41,
    a2: (unsigned int)&v37,
    a3: (unsigned int)&qword_141B5ACC8,
    a4: (unsigned int)v45,
    a5: 0,
    a6: 0);
  result = v41;
  if ( v41 == 0 )
    goto LABEL_61;
  v45[0] = v41;
  _InterlockedIncrement((volatile signed __int32 *)(v41 + 8));
  result = sub_1407C5A20(a1: &v35, a2: v45, a3: &v37, a4: &qword_141B5ACC8);
  v9 = (__int64 (__fastcall ***)(_QWORD, __int64))v45[0];
  if ( v45[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v45[0] + 8LL)) == 0 )
    result = (**v9)(a1: v9, a2: 1);
  v10 = v35;
  if ( v35 == 0 )
    goto LABEL_58;
  v42 = a1 + 5559;
  v34 = nullptr;
  sub_1407D8AB0(a1: v45, a2: 0x14191EB1BLL);
  (*(void (__fastcall **)(__int64, _QWORD *, __int64 *, _QWORD *, volatile signed __int32 **, int))(*(_QWORD *)v10
                                                                                                  + 216LL))(
    a1: v10,
    a2: v43,
    a3: &qword_141B59758,
    a4: v45,
    a5: &v34,
    a6: 1);
  v11 = v35;
  sub_1407D8AB0(a1: v45, a2: 0x1418EEAE0LL);
  result = (*(__int64 (__fastcall **)(__int64, _QWORD *, __int64 *, _QWORD *, volatile signed __int32 **, int))(*(_QWORD *)v11 + 216LL))(
             a1: v11,
             a2: v43,
             a3: &qword_141B59758,
             a4: v45,
             a5: &v34,
             a6: 1);
  if ( v34 == nullptr )
    goto LABEL_55;
  result = ((__int64 (*)(void))sub_1404B4FD0)();
  if ( result == 0 )
    goto LABEL_52;
  v12 = a1 + 5553;
  v13 = 0;
  while ( 1 )
  {
    sub_1407D4680(a1: v34, a2: &v36, a3: v13);
    sub_1407D0D60(a1: v39);
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v36 + 24LL))(a1: v36, a2: v45);
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v36 + 16LL))(a1: v36, a2: v43);
    sub_1407D0F70(
      a1: (unsigned int)v39,
      a2: (unsigned int)&v32,
      a3: (unsigned int)&v35,
      a4: (unsigned int)v43,
      a5: (__int64)v45,
      a6: 0,
      a7: 0,
      a8: 0);
    sub_140808B00(a1: v43);
    v14 = v32;
    if ( v32 == nullptr )
      goto LABEL_41;
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v32 + 40LL))(
               a1: v32,
               a2: &v31,
               a3: 1);
    if ( *((_DWORD *)v14 + 4) != 0 )
      goto LABEL_46;
    if ( v31 != 9 )
      break;
    v15 = v32;
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v32 + 40LL))(
               a1: v32,
               a2: v44,
               a3: 4);
    if ( *((_DWORD *)v15 + 4) != 0 )
      goto LABEL_46;
    v16 = v3;
    v17 = sub_1407E4940();
    v18 = (_QWORD *)sub_1407E4490(a1: v17, a2: 24);
    if ( qword_141ABD470 == 0 )
      qword_141ABD470 = sub_1407E4940();
    v18[2] = 0;
    v18[1] = 0;
    *v18 = 0;
    v45[0] = v18;
    v43[0] = v32;
    if ( v32 != nullptr )
      _InterlockedIncrement(v32 + 2);
    result = sub_140059500(a1: v38, a2: v43, a3: v18, a4: v33);
    v19 = v38[0];
    v20 = (__int64 (__fastcall ***)(_QWORD, __int64))v43[0];
    if ( v43[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v43[0] + 8LL)) == 0 )
      result = (**v20)(a1: v20, a2: 1);
    if ( v19 != 0 )
      goto LABEL_46;
    v3 = v16;
    sub_14000FD00(a1: v42, a2: v45, a3: v44[0]);
    v21 = v32;
    if ( v32 != nullptr )
      goto LABEL_39;
LABEL_41:
    v24 = v36;
    if ( v36 != nullptr && _InterlockedDecrement(v36 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v24)(a1: v24, a2: 1);
    ++v13;
    result = sub_1404B4FD0(a1: v34);
    if ( v13 >= result )
      goto LABEL_52;
  }
  v22 = v32;
  result = (*(__int64 (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v32 + 40LL))(
             a1: v32,
             a2: v33,
             a3: 2);
  if ( *((_DWORD *)v22 + 4) != 0 )
    goto LABEL_46;
  if ( v40 >= 4u )
  {
    v23 = v32;
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v32 + 40LL))(
               a1: v32,
               a2: v45,
               a3: 1);
    if ( *((_DWORD *)v23 + 4) != 0 )
      goto LABEL_46;
  }
  sub_14083D2C0(a1: v38);
  sub_1408386A0(a1: v32, a2: v45, a3: v38);
  if ( LODWORD(v45[0]) != 0 )
    goto LABEL_45;
  sub_1407C9510(a1: v43);
  sub_140839290(a1: v32, a2: v45, a3: v43);
  if ( LODWORD(v45[0]) == 0 )
  {
    sub_140A2DC30(a1: (unsigned int)v45, a2: (unsigned int)v43, a3: 0, a4: 0, a5: 0);
    if ( sub_140A2DD50(a1: v45) != 0 )
    {
      sub_1406292B0(a1: v45, a2: v3);
      sub_140A34040(a1: v45, a2: 0);
    }
    sub_14083DDA0(a1: v44, a2: v43);
    sub_14083B5F0(a1: v12, a2: v44);
    sub_14083D320(a1: v44);
    sub_140833970(a1: v43);
    sub_14083D320(a1: v38);
    v21 = v32;
    if ( v32 == nullptr )
      goto LABEL_41;
LABEL_39:
    if ( _InterlockedDecrement(v21 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v21)(a1: v21, a2: 1);
    goto LABEL_41;
  }
  sub_140833970(a1: v43);
LABEL_45:
  result = sub_14083D320(a1: v38);
LABEL_46:
  v25 = v32;
  if ( v32 != nullptr && _InterlockedDecrement(v32 + 2) == 0 )
    result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v25)(a1: v25, a2: 1);
  v26 = v36;
  if ( v36 != nullptr && _InterlockedDecrement(v36 + 2) == 0 )
    result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v26)(a1: v26, a2: 1);
LABEL_52:
  v27 = v34;
  if ( v34 != nullptr && _InterlockedDecrement(v34) == 0 )
  {
    sub_1400532D0(a1: v27);
    result = sub_141750CFC(a1: v27);
  }
LABEL_55:
  v28 = (__int64 (__fastcall ***)(_QWORD, __int64))v35;
  if ( v35 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v35 + 8)) == 0 )
    result = (**v28)(a1: v28, a2: 1);
LABEL_58:
  v29 = (__int64 (__fastcall ***)(_QWORD, __int64))v41;
  if ( v41 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v41 + 8)) == 0 )
    result = (**v29)(a1: v29, a2: 1);
LABEL_61:
  v30 = (__int64 (__fastcall ***)(_QWORD, __int64))v37;
  if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 + 8)) == 0 )
    return (**v30)(a1: v30, a2: 1);
  return result;
}
