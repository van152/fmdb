_DWORD *__fastcall sub_140839480(_DWORD *a1, _DWORD *a2, _QWORD *a3)
{
  _QWORD *v3; // rbx
  _DWORD *v4; // rsi
  _QWORD *v6; // r12
  _QWORD *v7; // rdi
  void (__fastcall *v8)(__int64, _QWORD *); // r15
  _QWORD *v9; // r14
  _QWORD *v10; // rsi
  __int64 v11; // rbx
  __int64 v12; // rsi
  __int64 v13; // rdi
  __int64 v14; // r15
  int v15; // eax
  __int64 *v16; // r12
  __int64 v17; // rsi
  __int64 v18; // r14
  __int64 v19; // rbx
  unsigned __int64 v20; // rcx
  __int64 v21; // r8
  __int64 v22; // rcx
  __int64 v23; // r12
  __int64 v24; // rcx
  bool v25; // al
  _QWORD *v27; // r15
  unsigned __int64 v28; // rbx
  __int64 v29; // rax
  _QWORD v30[2]; // [rsp+20h] [rbp-30h] BYREF
  int v31; // [rsp+30h] [rbp-20h] BYREF
  _DWORD *v32; // [rsp+38h] [rbp-18h]
  _QWORD *v33; // [rsp+40h] [rbp-10h]
  unsigned int v34; // [rsp+4Ch] [rbp-4h] BYREF
  __int64 v35; // [rsp+50h] [rbp+0h]

  v35 = -2;
  v3 = a3;
  v4 = a2;
  v6 = (_QWORD *)*a3;
  v7 = (_QWORD *)a3[1];
  if ( (_QWORD *)*a3 != v7 )
  {
    v33 = a3;
    v32 = a2;
    v8 = (void (__fastcall *)(__int64, _QWORD *))MEMORY[0x1419475D8];
    v9 = v6;
    do
    {
      v10 = (_QWORD *)*v9;
      if ( *v9 != 0 )
      {
        (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v10 + 16LL))(a1: *v10, a2: *v9);
        v11 = sub_140836BC0();
        v8(a1: v11 + 32, a2: v10);
        if ( (*(_BYTE *)(v11 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v11 + 64)) == 0)
          && *(_BYTE *)(v11 + 97) != 0 )
        {
          sub_1412D33C0(a1: v11);
        }
      }
      ++v9;
    }
    while ( v9 != v7 );
    v3 = v33;
    v12 = v33[1] - (_QWORD)v7;
    sub_141758A00(a1: v6, a2: v7, a3: v12);
    v33[1] = (char *)v6 + v12;
    v4 = v32;
  }
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: &v34, a3: 4);
  if ( a1[4] != 0 )
    goto LABEL_22;
  v13 = v34;
  if ( qword_141AA7808 <= (unsigned __int64)v34 )
  {
    a1[4] = 1;
LABEL_22:
    *v4 = 1;
    return v4;
  }
  v14 = *v3;
  v33 = v3;
  v15 = 0;
  if ( (v3[2] - v14) >> 3 < (unsigned __int64)v34 )
  {
    v32 = v4;
    v16 = v33;
    v17 = v33[1];
    v18 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v34);
    sub_141758A00(a1: v18, a2: *v16, a3: v16[1] - *v16);
    v19 = *v33;
    if ( *v33 != 0 )
    {
      v20 = v33[2] - v19;
      if ( v20 == -1 )
        v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v21 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20)
        && (v22 = *(_QWORD *)(v21 + 8 * v20)) != 0 )
      {
        v23 = v22;
        MEMORY[0x1419475D8](a1: v22 + 32, a2: v19 - *(unsigned int *)(v22 + 120));
        v24 = v23;
        v25 = *(_BYTE *)(v23 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 + 64)) != 0;
        v16 = v33;
        if ( !v25 && *(_BYTE *)(v24 + 97) != 0 )
          sub_1412D33C0(a1: v24);
      }
      else
      {
        MEMORY[0x141948990](a1: v19 - *(unsigned int *)(qword_141ABD470 + 48));
        v16 = v33;
      }
    }
    *v16 = v18;
    v16[1] = v18 + v17 - v14;
    v16[2] = v18 + 8 * v13;
    LODWORD(v13) = v34;
    v15 = a1[4];
    v4 = v32;
  }
  if ( (_DWORD)v13 == 0 || (v27 = v33, v15 != 0) )
  {
LABEL_32:
    *v4 = v15;
  }
  else
  {
    v28 = 1;
    while ( 1 )
    {
      v29 = sub_14083D4F0();
      v30[1] = 0;
      v30[0] = v29 + 8;
      sub_1408386A0(a1, a2: &v31, a3: v30);
      if ( v31 != 0 )
        break;
      sub_14083B5F0(a1: v27, a2: v30);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v30[0] + 16LL))(a1: v30[0], a2: v30);
      v15 = a1[4];
      if ( v28 < v34 )
      {
        ++v28;
        if ( v15 == 0 )
          continue;
      }
      goto LABEL_32;
    }
    *v4 = 1;
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v30[0] + 16LL))(a1: v30[0], a2: v30);
  }
  return v4;
}
