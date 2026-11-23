void __fastcall sub_14101E230(__int64 a1, _QWORD *a2)
{
  _QWORD *v2; // r12
  _QWORD *v4; // rax
  _QWORD *v5; // rax
  __int64 v6; // r13
  __int64 v7; // rdi
  unsigned __int64 v8; // r13
  __int64 v9; // rdi
  __int64 v10; // rbx
  char v11; // bl
  __int64 v12; // rbx
  __int64 v13; // rsi
  unsigned __int64 v14; // rcx
  __int64 v15; // rdi
  __int64 v16; // rdi
  bool v17; // al
  _QWORD *v18; // rsi
  __int64 v19; // rsi
  unsigned __int64 v20; // rcx
  __int64 v21; // rdi
  __int64 v22; // rdi
  bool v23; // al
  _QWORD *v24; // rsi
  __int64 v25; // rcx
  __int64 v26; // rax
  __int64 v27; // rcx
  __int64 v28; // rax
  __int64 v29; // [rsp+20h] [rbp-30h] BYREF
  __int64 v30; // [rsp+28h] [rbp-28h] BYREF
  __int64 v31; // [rsp+38h] [rbp-18h] BYREF
  int v32; // [rsp+40h] [rbp-10h]
  _QWORD *v33; // [rsp+48h] [rbp-8h]
  __int64 v34; // [rsp+50h] [rbp+0h]

  v34 = -2;
  if ( a2 == nullptr )
    return;
  v2 = a2;
  if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) == 3 )
  {
    v4 = (_QWORD *)v2[3];
    if ( v4 == (_QWORD *)v2[4] )
      goto LABEL_8;
    v5 = (_QWORD *)*v4;
    if ( v5 == nullptr )
      goto LABEL_8;
  }
  else
  {
    v5 = v2;
  }
  v2 = v5;
LABEL_8:
  v6 = *(_QWORD *)(a1 + 440) - *(_QWORD *)(a1 + 432);
  if ( v6 != 0 )
  {
    v7 = v6 >> 3;
    v8 = v6 & 0xFFFFFFFFFFFFFFF8uLL;
    v9 = -v7;
    while ( 1 )
    {
      v10 = *(_QWORD *)(*(_QWORD *)(a1 + 432) + v8 - 8);
      if ( v10 != 0 )
      {
        (*(void (__fastcall **)(_QWORD *, __int64 *))(*v2 + 144LL))(v2, &v29);
        v11 = sub_140FEB670(v10, (__int64)&v29);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v30 + 16LL))(v30, &v30);
        if ( v11 != 0 )
          break;
      }
      v8 -= 8LL;
      if ( ++v9 == 0 )
        goto LABEL_36;
    }
    v12 = *(_QWORD *)(*(_QWORD *)(a1 + 432) + v8 - 8);
    if ( v12 != 0 )
    {
      v13 = *(_QWORD *)(v12 + 56);
      if ( v13 != 0 )
      {
        v14 = *(_QWORD *)(v12 + 72) - v13;
        if ( v14 == -1 )
          v14 = *(unsigned int *)(v13 - *(unsigned int *)(qword_141ABD470 + 48));
        v33 = (_QWORD *)(v12 + 56);
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v15 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v15) >> 3 > v14)
          && (v16 = *(_QWORD *)(v15 + 8 * v14)) != 0 )
        {
          MEMORY[0x1419475D8](v16 + 32, v13 - *(unsigned int *)(v16 + 120));
          v17 = *(_BYTE *)(v16 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 64)) != 0;
          v18 = v33;
          if ( !v17 && *(_BYTE *)(v16 + 97) != 0 )
            sub_1412D33C0(v16);
        }
        else
        {
          MEMORY[0x141948990](v13 - *(unsigned int *)(qword_141ABD470 + 48));
          v18 = v33;
        }
        v18[2] = 0;
        v18[1] = 0;
        *v18 = 0;
      }
      v19 = *(_QWORD *)(v12 + 24);
      if ( v19 != 0 )
      {
        v20 = *(_QWORD *)(v12 + 40) - v19;
        if ( v20 == -1 )
          v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
        v33 = (_QWORD *)(v12 + 24);
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v21 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20)
          && (v22 = *(_QWORD *)(v21 + 8 * v20)) != 0 )
        {
          MEMORY[0x1419475D8](v22 + 32, v19 - *(unsigned int *)(v22 + 120));
          v23 = *(_BYTE *)(v22 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) != 0;
          v24 = v33;
          if ( !v23 && *(_BYTE *)(v22 + 97) != 0 )
            sub_1412D33C0(v22);
        }
        else
        {
          MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
          v24 = v33;
        }
        v24[2] = 0;
        v24[1] = 0;
        *v24 = 0;
      }
      (*(void (__fastcall **)(_QWORD, __int64))(**(_QWORD **)(v12 + 8) + 16LL))(*(_QWORD *)(v12 + 8), v12 + 8);
      sub_141750CFC(v12);
    }
    sub_141758A00();
    *(_QWORD *)(a1 + 440) -= 8LL;
  }
LABEL_36:
  sub_1407C9510(&v29);
  v26 = sub_14083D4F0(v25);
  v32 = 1853059955;
  v31 = v26 + 56;
  sub_14083B5F0(&v29, &v31);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, &v31);
  v28 = sub_14083D4F0(v27);
  v32 = 1935829358;
  v31 = v28 + 56;
  sub_14083B5F0(&v29, &v31);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, &v31);
  (*(void (__fastcall **)(__int64, __int64, _QWORD *, __int64 *))(*(_QWORD *)qword_141B5EF38 + 56LL))(
    qword_141B5EF38,
    a1,
    v2,
    &v29);
  sub_14083B0A0(&v29);
}
