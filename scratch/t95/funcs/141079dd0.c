// THUNK ALIAS -> sub_143F1E600 (jmp:0x141079dd0->0x143f1e600)
__int64 __fastcall sub_143F1E600(__int64 **a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rdx
  unsigned __int64 v8; // rdi
  __int64 v9; // r13
  __int64 v10; // rsi
  __int64 v11; // r15
  unsigned __int64 v12; // rcx
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v17; // r8
  __int64 v18; // rcx
  __int64 v19; // rbx
  __int64 v20; // rsi
  __int64 v21; // rax
  __int64 v22; // [rsp+20h] [rbp-30h]
  __int64 v23; // [rsp+28h] [rbp-28h] BYREF
  __int64 v24; // [rsp+30h] [rbp-20h]
  unsigned __int64 v25; // [rsp+38h] [rbp-18h]
  __int64 v26; // [rsp+40h] [rbp-10h] BYREF
  __int64 v27; // [rsp+48h] [rbp-8h]
  __int64 v28; // [rsp+50h] [rbp+0h]

  v28 = -2;
  sub_1407C9510(&v23);
  v4 = **a1;
  v5 = *(_QWORD *)(v4 + 288);
  v6 = *(_QWORD *)(v4 + 296);
  v7 = v6 - v5;
  v8 = (v6 - v5) >> 4;
  v9 = v23;
  if ( (__int64)(v25 - v23) >> 3 >= v8 )
  {
    if ( v6 == v5 )
      goto LABEL_8;
    goto LABEL_19;
  }
  if ( v7 < 0 )
    sub_1400526C0(v6);
  v10 = v24;
  v11 = sub_1407E4490(qword_141ABD470, (unsigned __int64)v7 >> 1);
  sub_141758A00();
  if ( v23 != 0 )
  {
    v12 = v25 - v23;
    if ( v25 - v23 == -1 )
    {
      v12 = *(unsigned int *)(v23 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_17:
        MEMORY[0x141948990](v23 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_18;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_17;
    }
    v17 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v12 )
    {
      v18 = *(_QWORD *)(v17 + 8 * v12);
      if ( v18 != 0 )
      {
        v22 = v18;
        MEMORY[0x1419475D8](v18 + 32, v23 - *(unsigned int *)(v18 + 120));
        v6 = v22;
        if ( (*(_BYTE *)(v22 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) == 0)
          && *(_BYTE *)(v22 + 97) != 0 )
        {
          sub_1412D33C0(v22);
        }
        goto LABEL_18;
      }
    }
    goto LABEL_17;
  }
LABEL_18:
  v23 = v11;
  v24 = v11 + v10 - v9;
  v25 = v11 + 8 * v8;
LABEL_19:
  v19 = 0;
  do
  {
    v20 = *(_QWORD *)(**a1 + 288);
    if ( v20 != 0 )
    {
      v21 = sub_14083D4F0(v6);
      v27 = 0;
      v26 = v21 + 8;
      sub_1410762A0(v19 + v20, &v26);
      sub_14083B5F0(&v23, &v26);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v26 + 16LL))(v26, &v26);
    }
    v19 += 16;
    --v8;
  }
  while ( v8 != 0 );
LABEL_8:
  sub_14083DB80(&v26, &v23);
  v13 = *a2;
  if ( &v26 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, a2);
    v14 = v26;
    v15 = v27;
    a2[1] = v27;
    *a2 = v14;
    v13 = sub_14083D4F0(v15) + 8;
    v27 = 0;
    v26 = v13;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, &v26);
  return sub_14083B0A0(&v23);
}
