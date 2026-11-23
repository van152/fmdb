__int64 __fastcall sub_140EDFB90(__int64 a1, __int64 *a2)
{
  __int64 v2; // rdi
  __int64 v3; // rax
  unsigned int *v4; // r13
  __int64 *v5; // r12
  unsigned int **v6; // r15
  __int64 v7; // r8
  bool v8; // zf
  int *v9; // r12
  __int64 v10; // rbx
  unsigned __int64 i; // rdi
  __int64 v12; // r14
  unsigned int **v13; // r13
  __int64 v14; // r15
  int *v15; // rsi
  _QWORD *v16; // rbx
  _QWORD *v17; // r12
  unsigned __int64 v18; // rax
  __int64 v19; // rbx
  __int64 v20; // rcx
  unsigned int *v21; // r14
  unsigned int v22; // esi
  unsigned int *v23; // rsi
  __int64 v24; // r8
  __int64 v25; // rcx
  unsigned int *v27; // [rsp+40h] [rbp-40h]
  __int64 *v28; // [rsp+48h] [rbp-38h]
  __int64 v29; // [rsp+50h] [rbp-30h]
  unsigned int *v30; // [rsp+58h] [rbp-28h]
  __int64 *v31; // [rsp+60h] [rbp-20h]
  _QWORD **v32; // [rsp+68h] [rbp-18h]
  unsigned int *v33; // [rsp+70h] [rbp-10h]
  unsigned int v34; // [rsp+7Ch] [rbp-4h] BYREF
  __int64 v35; // [rsp+80h] [rbp+0h] BYREF
  unsigned int *v36; // [rsp+88h] [rbp+8h] BYREF
  __int64 v37; // [rsp+90h] [rbp+10h]
  __int64 *v38; // [rsp+98h] [rbp+18h]
  __int64 v39; // [rsp+A0h] [rbp+20h]

  v39 = -2;
  v2 = a1;
  v3 = *a2;
  v35 = v3;
  if ( v3 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v3 + 8));
  v36 = (unsigned int *)(a1 + 48);
  v37 = 12;
  v27 = (unsigned int *)(a1 + 60);
  v38 = (__int64 *)(a1 + 60);
  if ( v35 != 0 )
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: a1 + 48, a3: 12);
  v28 = (__int64 *)(v2 + 64);
  v36 = (unsigned int *)(v2 + 64);
  v37 = 8;
  v4 = (unsigned int *)(v2 + 72);
  v38 = (__int64 *)(v2 + 72);
  v5 = (__int64 *)(v2 + 76);
  if ( v35 != 0 )
    (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: 8);
  v6 = &v36;
  v36 = (unsigned int *)(v2 + 76);
  v37 = 6;
  v38 = (__int64 *)(v2 + 82);
  sub_140EDF3C0(a1: v2 + 40);
  v34 = 0;
  v33 = (unsigned int *)(v2 + 82);
  if ( (unsigned int *)(v2 + 82) == &v34 )
  {
    v8 = v37 == -4;
    v7 = v37 + 4;
    v37 += 4;
    v38 = &v35;
    if ( v8 )
      goto LABEL_15;
  }
  else
  {
    if ( v37 != 0 && v35 != 0 )
      (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: v37);
    v36 = &v34;
    v37 = 4;
    v38 = &v35;
    v7 = 4;
  }
  if ( v35 != 0 )
    (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: v7);
LABEL_15:
  v38 = nullptr;
  v37 = 0;
  v36 = nullptr;
  v32 = (_QWORD **)(v2 + 40);
  if ( v34 == 0 )
  {
    v21 = (unsigned int *)(v2 + 90);
    goto LABEL_43;
  }
  v31 = (__int64 *)(v2 + 76);
  v30 = (unsigned int *)(v2 + 72);
  v29 = v2;
  v9 = &dword_141B5D2E8;
  v10 = 0x76C0001076C0001LL;
  for ( i = 0; i < v34; ++i )
  {
    if ( unk_141B5D338 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                     + (unsigned int)qword_141AC5D50)
                                   + 4LL) )
    {
      sub_141750E08(a1: &unk_141B5D338);
      if ( unk_141B5D338 == -1 )
      {
        sub_1407E53D0(a1: (_DWORD)v9, a2: 1100129537, a3: 512, a4: 28, a5: 0, a6: 0, a7: 512, a8: 0);
        sub_141751048(a1: &qword_140E40E78[47]);
        sub_141750EA0(a1: &unk_141B5D338);
      }
    }
    v12 = sub_1407E58C0(a1: v9, a2: 28);
    *(_QWORD *)v12 = v10;
    *(_QWORD *)(v12 + 8) = -1;
    *(_QWORD *)(v12 + 16) = 0;
    *(_DWORD *)(v12 + 24) = 0;
    if ( v37 != 0 && v35 != 0 )
      (*(void (__fastcall **)(__int64, unsigned int *))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36);
    v6[2] = nullptr;
    v6[1] = nullptr;
    *v6 = nullptr;
    if ( (unsigned __int8)sub_1414C4670(a1: v12, a2: &v35) == 0 )
    {
      sub_140E40D00(a1: v12);
      v22 = 0;
      goto LABEL_58;
    }
    if ( *(_WORD *)(v12 + 22) == 613 )
    {
      sub_140E40D00(a1: v12);
    }
    else
    {
      v13 = v6;
      v14 = v10;
      v15 = v9;
      v16 = v32;
      v17 = *v32;
      if ( *v32 == nullptr )
      {
        if ( dword_141B59A98 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                           + (unsigned int)qword_141AC5D50)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59A98);
          if ( dword_141B59A98 == -1 )
          {
            sub_1407E3E70(a1: &qword_141B59A58);
            sub_141751048(a1: &qword_1407E49F8[35]);
            sub_141750EA0(a1: &dword_141B59A98);
            v16 = v32;
          }
        }
        v17 = (_QWORD *)sub_1407E4490(a1: &qword_141B59A58, a2: 96);
        *v17 = 0;
        v17[1] = 0;
        v17[2] = 0;
        v17[3] = 0;
        v17[4] = 0;
        v17[5] = 0;
        v17[6] = 0;
        v17[7] = 0;
        v17[8] = 0;
        v17[9] = 0;
        v17[10] = 0;
        v17[11] = 0;
        *v16 = v17;
      }
      v18 = *(unsigned __int8 *)v17;
      if ( v18 > 9 )
      {
        v19 = *((unsigned __int8 *)v17 + 88);
        v20 = v17[v19 + 1];
        if ( v20 != 0 )
          sub_140E40D00(a1: v20);
        v17[v19 + 1] = v12;
        if ( (unsigned __int8)(*((_BYTE *)v17 + 88) + 1) < 0xAu )
          JUMPOUT(0x140EDFEDFLL);
        *((_BYTE *)v17 + 88) = 0;
      }
      else
      {
        v17[v18 + 1] = v12;
        *(_BYTE *)v17 = v18 + 1;
      }
      v9 = v15;
      v10 = v14;
      v6 = v13;
    }
  }
  v2 = v29;
  v21 = (unsigned int *)(v29 + 90);
  if ( v38 != (__int64 *)(v29 + 90) )
  {
    v4 = v30;
    v5 = v31;
LABEL_43:
    v23 = v33;
    if ( v37 != 0 && v35 != 0 )
      (*(void (__fastcall **)(__int64, unsigned int *))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36);
    v36 = v21;
    v37 = 1;
    v38 = (__int64 *)(v2 + 91);
    v24 = 1;
    goto LABEL_47;
  }
  v24 = v37 + 1;
  v8 = v37++ == -1;
  v38 = (__int64 *)(v29 + 91);
  v4 = v30;
  v5 = v31;
  v23 = v33;
  if ( v8 )
  {
LABEL_49:
    v36 = v27;
    v37 = 4;
    v38 = v28;
    if ( v35 != 0 )
      (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: 4);
    goto LABEL_51;
  }
LABEL_47:
  if ( v35 != 0 )
  {
    (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: v24);
    goto LABEL_49;
  }
LABEL_51:
  v36 = v23;
  v37 = 7;
  v38 = (__int64 *)(v2 + 89);
  if ( v35 != 0 )
  {
    (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: 7);
    v36 = (unsigned int *)(v2 + 32);
    v37 = 8;
    v38 = (__int64 *)v32;
    if ( v35 != 0 )
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v2 + 32, a3: 8);
  }
  v36 = v4;
  v37 = 4;
  v38 = v5;
  if ( v35 != 0 )
  {
    (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: 4);
    v36 = (unsigned int *)(v2 + 89);
    v37 = 1;
    v38 = (__int64 *)v21;
    if ( v35 != 0 )
      (*(void (__fastcall **)(__int64, unsigned int *, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36, a3: 1);
  }
  v6[2] = nullptr;
  v6[1] = nullptr;
  *v6 = nullptr;
  v22 = sub_140E4EC20(a1: v2, a2: &v35, a3: v24);
LABEL_58:
  if ( v37 != 0 )
  {
    if ( v35 == 0 )
      return v22;
    (*(void (__fastcall **)(__int64, unsigned int *))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v36);
  }
  v25 = v35;
  v6[2] = nullptr;
  v6[1] = nullptr;
  *v6 = nullptr;
  if ( v25 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v25)(a1: v25, a2: 1);
  return v22;
}
