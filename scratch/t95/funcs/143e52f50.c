__int64 __fastcall sub_143E52F50(__int64 a1, int a2)
{
  char *v4; // rdx
  __int64 v5; // rbx
  __int64 v6; // r14
  unsigned __int64 v8; // rbx
  __int64 v9; // rdi
  char *v10; // rax
  char *v11; // r8
  char *v12; // rax
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rdx
  __int64 v16; // rdi
  __int64 v17; // rcx
  _DWORD v18[2]; // [rsp+20h] [rbp-60h] BYREF
  __int64 v19; // [rsp+28h] [rbp-58h]
  __int64 v20; // [rsp+30h] [rbp-50h]
  __int64 v21; // [rsp+38h] [rbp-48h]
  __int64 v22; // [rsp+40h] [rbp-40h]
  __int64 v23; // [rsp+48h] [rbp-38h]
  __int64 v24; // [rsp+50h] [rbp-30h]
  __int64 v25; // [rsp+58h] [rbp-28h]
  __int64 v26; // [rsp+60h] [rbp-20h]
  __int64 v27; // [rsp+68h] [rbp-18h]
  __int64 v28; // [rsp+70h] [rbp-10h]
  __int64 v29; // [rsp+78h] [rbp-8h]
  __int64 v30; // [rsp+80h] [rbp+0h]
  __int64 v31; // [rsp+88h] [rbp+8h]
  __int64 v32; // [rsp+90h] [rbp+10h]
  __int64 v33; // [rsp+98h] [rbp+18h]
  __int64 v34; // [rsp+A0h] [rbp+20h]
  __int64 v35; // [rsp+A8h] [rbp+28h]
  __int64 v36; // [rsp+B0h] [rbp+30h]
  int v37; // [rsp+B8h] [rbp+38h]
  __int64 v38; // [rsp+C0h] [rbp+40h]

  v38 = -2;
  v18[0] = -1;
  v19 = 0;
  v20 = 0;
  v21 = 0;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v37 = 0;
  v36 = 0;
  v35 = 0;
  v34 = 0;
  v33 = 0;
  v32 = 0;
  v31 = 0;
  v30 = 0;
  v29 = 0;
  v28 = 0;
  v27 = 0;
  v26 = 0;
  v25 = 0;
  v24 = 0;
  v23 = 0;
  v22 = 0;
  v18[1] = a2;
  v4 = *(char **)(a1 + 32);
  v5 = *(_QWORD *)(a1 + 40) - (_QWORD)v4;
  if ( v5 < 8 )
    goto LABEL_5;
  v8 = (unsigned __int64)v5 >> 3;
  v6 = 0;
  v9 = v8;
  while ( 1 )
  {
    v9 = (unsigned __int64)v9 >> 1;
    v10 = &v4[8 * v9];
    if ( *(_DWORD *)(*(_QWORD *)v10 + 4LL) >= a2 )
      break;
    v9 = v8 + ~v9;
    v4 = v10 + 8;
LABEL_9:
    v8 = v9;
    if ( v9 <= 0 )
      goto LABEL_6;
  }
  if ( *(_DWORD *)(*(_QWORD *)v10 + 4LL) > a2 )
    goto LABEL_9;
  v11 = v4;
  if ( v8 >= 2 )
  {
    v16 = v9 & 0x1FFFFFFFFFFFFFFFLL;
    v11 = v4;
    v17 = v16;
    do
    {
      v17 = (unsigned __int64)v17 >> 1;
      if ( *(_DWORD *)(*(_QWORD *)&v11[8 * v17] + 4LL) < a2 )
      {
        v11 += 8 * v17 + 8;
        v17 = v16 + ~v17;
      }
      v16 = v17;
    }
    while ( v17 > 0 );
  }
  v12 = v10 + 8;
  v13 = &v4[8 * v8] - v12;
  if ( v13 > 0 )
  {
    v14 = (unsigned __int64)v13 >> 3;
    v15 = v14;
    do
    {
      v15 = (unsigned __int64)v15 >> 1;
      if ( *(_DWORD *)(*(_QWORD *)&v12[8 * v15] + 4LL) <= a2 )
      {
        v12 += 8 * v15 + 8;
        v15 = v14 + ~v15;
      }
      v14 = v15;
    }
    while ( v15 > 0 );
  }
  if ( v11 != v12 )
  {
    v6 = *(_QWORD *)v11;
    goto LABEL_6;
  }
LABEL_5:
  v6 = 0;
LABEL_6:
  sub_140FF5030(v18);
  return v6;
}
