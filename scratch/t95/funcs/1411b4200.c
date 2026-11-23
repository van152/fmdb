char __fastcall sub_1411B4200(__int64 a1, __int64 a2)
{
  __int64 *v4; // rdx
  __int64 v5; // r8
  __int64 v6; // rsi
  char v7; // cl
  __int64 v8; // rbx
  __int64 v9; // rax
  char v10; // cl
  __int64 *v11; // rdi
  char *v12; // rdx
  int v13; // r15d
  int v14; // r11d
  int v15; // ecx
  int v16; // edi
  int v17; // r12d
  int v18; // r9d
  int v19; // r13d
  int v20; // r10d
  char v21; // r14
  int v22; // r8d
  int v23; // edx
  __int64 v24; // rbx
  unsigned __int64 v25; // rcx
  __int64 v26; // rdx
  unsigned __int64 v27; // rax
  __int64 v28; // rdi
  unsigned __int64 v29; // rcx
  __int64 v30; // rsi
  __int64 v31; // r14
  bool v32; // al
  char result; // al
  __int64 v34; // rsi
  unsigned __int64 v35; // rcx
  __int64 v36; // rdx
  __int64 v37; // rdi
  unsigned __int64 v38; // [rsp+20h] [rbp-60h]
  __int64 v39; // [rsp+28h] [rbp-58h]
  __int64 v40; // [rsp+30h] [rbp-50h]
  __int64 *v41; // [rsp+38h] [rbp-48h]
  int v42; // [rsp+48h] [rbp-38h]
  int v43; // [rsp+50h] [rbp-30h]
  int v44; // [rsp+54h] [rbp-2Ch]
  int v45; // [rsp+58h] [rbp-28h]
  int v46; // [rsp+5Ch] [rbp-24h]
  int v47; // [rsp+60h] [rbp-20h]
  int v48; // [rsp+64h] [rbp-1Ch]
  __int64 v49; // [rsp+68h] [rbp-18h]
  __int128 v50; // [rsp+70h] [rbp-10h] BYREF
  __int64 v51; // [rsp+80h] [rbp+0h]
  int v52; // [rsp+90h] [rbp+10h]
  int v53; // [rsp+94h] [rbp+14h]
  int v54; // [rsp+98h] [rbp+18h]
  int v55; // [rsp+9Ch] [rbp+1Ch]
  __int64 v56; // [rsp+A0h] [rbp+20h]
  char v57; // [rsp+AEh] [rbp+2Eh]
  char v58; // [rsp+AFh] [rbp+2Fh]
  __int64 v59; // [rsp+B0h] [rbp+30h]

  v59 = -2;
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
  v50 = 0;
  v51 = 0;
  if ( sub_140FE35F0() == 0 )
    return sub_1415EAED0(&v50, a2);
  v4 = *(__int64 **)(*(_QWORD *)(a1 + 160) + 168LL);
  if ( v4 == nullptr )
    return sub_1415EAED0(&v50, a2);
  v5 = *v4;
  v6 = v4[1];
  if ( v6 == *v4 )
    return sub_1415EAED0(&v50, a2);
  v40 = a2;
  v7 = 1;
  v49 = 0;
  v8 = 0;
  v9 = 0;
  v41 = v4;
  do
  {
    v12 = *(char **)(v6 - 8);
    v6 -= 8;
    if ( v12 != nullptr )
    {
      v58 = v7;
      v52 = v12[162];
      v13 = v12[155];
      v53 = v12[163];
      v14 = v12[156];
      v54 = v12[164];
      v15 = v12[157];
      v55 = v12[165];
      v16 = v12[158];
      v17 = v12[166];
      v18 = v12[159];
      v19 = v12[167];
      v20 = v12[160];
      v21 = v12[261];
      v22 = v12[168];
      v23 = v12[161];
      if ( v9 != v8 )
      {
        *(_DWORD *)v9 = v13;
        *(_DWORD *)(v9 + 4) = v14;
        *(_DWORD *)(v9 + 8) = v15;
        *(_DWORD *)(v9 + 12) = v16;
        *(_DWORD *)(v9 + 16) = v18;
        *(_DWORD *)(v9 + 20) = v20;
        *(_DWORD *)(v9 + 24) = v23;
        *(_DWORD *)(v9 + 28) = v52;
        *(_DWORD *)(v9 + 32) = v53;
        *(_DWORD *)(v9 + 36) = v54;
        *(_DWORD *)(v9 + 40) = v55;
        *(_DWORD *)(v9 + 44) = v17;
        *(_DWORD *)(v9 + 48) = v19;
        *(_DWORD *)(v9 + 52) = v22;
        v10 = v58;
        *(_BYTE *)(v9 + 56) = v58;
        *(_BYTE *)(v9 + 57) = v21;
        v9 += 60;
        *((_QWORD *)&v50 + 1) = v9;
        v11 = v41;
LABEL_9:
        v7 = v10 + 1;
        v5 = *v11;
        continue;
      }
      v48 = v23;
      v47 = v20;
      v46 = v18;
      v45 = v16;
      v44 = v15;
      v43 = v14;
      v42 = v22;
      v57 = v21;
      v56 = v6;
      v24 = v8 - v49;
      v25 = 0xEEEEEEEEEEEEEEEFuLL * (v24 >> 2);
      v26 = 0x444444444444444LL;
      v27 = v25 + (v25 >> 1);
      v38 = v25 + 1;
      if ( v27 <= v25 + 1 )
        v27 = v25 + 1;
      if ( v25 <= 0x444444444444444LL - (v25 >> 1) )
        v26 = v27;
      v39 = 60 * v26;
      v28 = sub_1407E4490(qword_141ABD470, 60 * v26);
      *(_DWORD *)(v28 + v24) = v13;
      *(_DWORD *)(v28 + v24 + 4) = v43;
      *(_DWORD *)(v28 + v24 + 8) = v44;
      *(_DWORD *)(v28 + v24 + 12) = v45;
      *(_DWORD *)(v28 + v24 + 16) = v46;
      *(_DWORD *)(v28 + v24 + 20) = v47;
      *(_DWORD *)(v28 + v24 + 24) = v48;
      *(_DWORD *)(v28 + v24 + 28) = v52;
      *(_DWORD *)(v28 + v24 + 32) = v53;
      *(_DWORD *)(v28 + v24 + 36) = v54;
      *(_DWORD *)(v28 + v24 + 40) = v55;
      *(_DWORD *)(v28 + v24 + 44) = v17;
      *(_DWORD *)(v28 + v24 + 48) = v19;
      *(_DWORD *)(v28 + v24 + 52) = v42;
      *(_BYTE *)(v28 + v24 + 56) = v58;
      *(_BYTE *)(v28 + v24 + 57) = v57;
      sub_141758A00();
      v6 = v56;
      if ( (_QWORD)v50 == 0 )
      {
LABEL_28:
        *(_QWORD *)&v50 = v28;
        v9 = v28 + 60 * v38;
        *((_QWORD *)&v50 + 1) = v9;
        v8 = v28 + v39;
        v51 = v28 + v39;
        v49 = v28;
        v11 = v41;
        v10 = v58;
        goto LABEL_9;
      }
      v29 = v51 - v50;
      if ( v51 - (_QWORD)v50 == -1 )
      {
        v29 = *(unsigned int *)(v50 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          goto LABEL_26;
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_26;
      }
      v30 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29 )
      {
        v31 = *(_QWORD *)(v30 + 8 * v29);
        if ( v31 != 0 )
        {
          MEMORY[0x1419475D8](v31 + 32, v50 - *(unsigned int *)(v31 + 120));
          v32 = *(_BYTE *)(v31 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) != 0;
          v6 = v56;
          if ( v32 || *(_BYTE *)(v31 + 97) == 0 )
            goto LABEL_28;
          sub_1412D33C0(v31);
          goto LABEL_27;
        }
      }
LABEL_26:
      MEMORY[0x141948990](v50 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_27:
      v6 = v56;
      goto LABEL_28;
    }
  }
  while ( v6 != v5 );
  v34 = v50;
  result = sub_1415EAED0(&v50, v40);
  if ( v34 != 0 )
  {
    v35 = v51 - v34;
    if ( v51 - v34 == -1 )
    {
      v35 = *(unsigned int *)(v34 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v34 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v34 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v36 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v36) >> 3 > v35 && (v37 = *(_QWORD *)(v36 + 8 * v35)) != 0 )
    {
      MEMORY[0x1419475D8](v37 + 32, v34 - *(unsigned int *)(v37 + 120));
      result = *(_BYTE *)(v37 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 + 64)) != 0;
      if ( result == 0 && *(_BYTE *)(v37 + 97) != 0 )
        return sub_1412D33C0(v37);
    }
    else
    {
      return MEMORY[0x141948990](v34 - *(unsigned int *)(qword_141ABD470 + 48));
    }
  }
  return result;
}
