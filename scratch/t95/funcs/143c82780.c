__int64 __fastcall sub_143C82780(_QWORD **a1, __int64 *a2)
{
  __int64 **v4; // rcx
  __int64 *v5; // rax
  __int64 *v6; // rcx
  __int64 v7; // rbx
  __int64 v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rdx
  unsigned __int64 v15; // rdi
  __int64 v16; // r13
  __int64 v17; // rsi
  __int64 v18; // r14
  unsigned __int64 v19; // rcx
  __int64 v20; // r8
  __int64 v21; // rcx
  bool v22; // al
  __int64 v23; // rbx
  __int64 *v24; // rcx
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 v27; // rsi
  __int64 v28; // rax
  __int64 v29; // [rsp+20h] [rbp-30h]
  __int64 v30; // [rsp+28h] [rbp-28h] BYREF
  __int64 v31; // [rsp+30h] [rbp-20h]
  unsigned __int64 v32; // [rsp+38h] [rbp-18h]
  __int64 v33; // [rsp+40h] [rbp-10h] BYREF
  __int64 v34; // [rsp+48h] [rbp-8h]
  __int64 v35; // [rsp+50h] [rbp+0h]

  v35 = -2;
  sub_1407C9510(&v30);
  v4 = *(__int64 ***)(qword_141B601E8 + 128);
  v5 = *v4;
  v6 = v4[1];
  if ( v5 != v6 )
  {
    while ( 1 )
    {
      v7 = *v5;
      if ( *(_QWORD *)(*v5 + 48) == **a1 )
        break;
      if ( ++v5 == v6 )
        goto LABEL_4;
    }
    v12 = *(_QWORD *)(v7 + 24);
    v13 = *(_QWORD *)(v7 + 32);
    v14 = v13 - v12;
    v15 = (v13 - v12) >> 3;
    v16 = v30;
    if ( (__int64)(v32 - v30) >> 3 >= v15 )
    {
      if ( v13 == v12 )
        goto LABEL_4;
    }
    else
    {
      if ( v14 < 0 )
        sub_1400526C0(v13);
      v17 = v31;
      v18 = sub_1407E4490(qword_141ABD470, v14);
      sub_141758A00();
      if ( v30 != 0 )
      {
        v19 = v32 - v30;
        if ( v32 - v30 == -1 )
          v19 = *(unsigned int *)(v30 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v20 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19)
          && (v21 = *(_QWORD *)(v20 + 8 * v19)) != 0 )
        {
          v29 = v21;
          MEMORY[0x1419475D8](v21 + 32, v30 - *(unsigned int *)(v21 + 120));
          v22 = *(_BYTE *)(v29 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) != 0;
          if ( !v22 && *(_BYTE *)(v29 + 97) != 0 )
            sub_1412D33C0(v29);
        }
        else
        {
          MEMORY[0x141948990](v30 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      v30 = v18;
      v31 = v18 + v17 - v16;
      v32 = v18 + 8 * v15;
    }
    v23 = 0;
    do
    {
      v24 = *(__int64 **)(qword_141B601E8 + 128);
      v25 = *v24;
      v26 = v24[1];
      if ( v25 != v26 )
      {
        while ( *(_QWORD *)(*(_QWORD *)v25 + 48LL) != **a1 )
        {
          v25 += 8;
          if ( v25 == v26 )
            goto LABEL_22;
        }
        v27 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)v25 + 24LL) + 8 * v23);
        if ( v27 != 0 )
        {
          v28 = sub_14083D4F0(v26);
          v34 = 0;
          v33 = v28 + 8;
          sub_140EB15D0(v27, &v33);
          sub_14083B5F0(&v30, &v33);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v33 + 16LL))(v33, &v33);
        }
      }
LABEL_22:
      ++v23;
    }
    while ( v23 != v15 );
  }
LABEL_4:
  sub_14083DB80(&v33, &v30);
  v8 = *a2;
  if ( &v33 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v8 + 16LL))(v8, a2);
    v9 = v33;
    v10 = v34;
    a2[1] = v34;
    *a2 = v9;
    v8 = sub_14083D4F0(v10) + 8;
    v34 = 0;
    v33 = v8;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v8 + 16LL))(v8, &v33);
  return sub_14083B0A0(&v30);
}
