__int64 __fastcall sub_1411A43E0(__int64 a1, char a2)
{
  __int64 v2; // rsi
  __int64 v4; // rsi
  int v5; // r15d
  __int64 v6; // r12
  __int64 v7; // r13
  __int64 v8; // r14
  __int64 v9; // rax
  __int64 v10; // rbx
  int v11; // eax
  unsigned int v12; // ecx
  int v13; // eax
  unsigned int v14; // edx
  int v15; // ecx
  int v16; // ecx
  int v17; // eax
  unsigned int v18; // ecx
  int v19; // eax
  unsigned int v20; // edx
  int v21; // ecx
  __int64 v22; // rax
  int v23; // ecx
  unsigned int v24; // ecx
  int v25; // eax
  unsigned int v26; // edx
  int v27; // ecx
  int v28; // ecx
  unsigned int v29; // edx
  int v30; // eax
  int v31; // eax
  unsigned int v32; // edx
  int v33; // ecx
  int v34; // ecx
  unsigned int v35; // edx
  unsigned int v36; // eax
  int v37; // edx
  int v38; // edx
  unsigned int v39; // ecx
  unsigned int v40; // eax
  int v41; // r9d
  int v42; // r9d
  unsigned int v43; // edx
  unsigned int v44; // ecx
  int v45; // r8d
  unsigned int v46; // ebx
  int v47; // edx
  unsigned int v48; // ecx
  int v49; // ebx
  unsigned int v50; // eax
  unsigned int v51; // ecx
  unsigned int v52; // ecx
  int v53; // eax
  unsigned int v54; // eax
  signed int v55; // eax
  __int64 v56; // rcx
  __int64 v57; // rsi
  unsigned __int64 v58; // rcx
  __int64 v59; // rbx
  __int64 v60; // rdi
  __int128 v62; // [rsp+20h] [rbp-30h]
  __int128 v63; // [rsp+30h] [rbp-20h] BYREF
  __int64 v64; // [rsp+40h] [rbp-10h]
  char v65; // [rsp+4Fh] [rbp-1h]
  __int64 v66; // [rsp+50h] [rbp+0h]

  v66 = -2;
  v2 = *(_QWORD *)(a1 + 48);
  if ( v2 == 0 )
    return 0;
  v65 = a2;
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
  v63 = 0;
  v64 = 0;
  sub_1411E5770(v2, &v63, 0, 0);
  v62 = v63;
  if ( *((_QWORD *)&v63 + 1) != (_QWORD)v63 )
  {
    v4 = 1;
    if ( (unsigned __int64)((__int64)(*((_QWORD *)&v63 + 1) - v63) >> 3) >= 2 )
      v4 = (__int64)(*((_QWORD *)&v63 + 1) - v63) >> 3;
    v5 = 0;
    v6 = 0;
    v7 = 0;
    while ( 1 )
    {
      v8 = *(_QWORD *)(v63 + 8 * v6);
      if ( v8 != 0 )
      {
        v9 = sub_140DE1C70(*(int *)(*(_QWORD *)(v8 + 8) + 8LL) + v8 + 344, *(_QWORD *)(a1 + 48), 0);
        if ( v9 != 0 )
        {
          v10 = v9;
          if ( (*(_BYTE *)(v9 + 28) & 0xFE) == 0x14 )
          {
            if ( *(_QWORD *)(v9 + 16) == a1 )
              goto LABEL_16;
          }
          else if ( ((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 104LL))(v9) & 0xFE) == 0x14
                 && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v10 + 88LL))(v10) == a1 )
          {
LABEL_16:
            switch ( v65 )
            {
              case 0:
                v11 = *(__int16 *)(v8 + 214);
                if ( v5 < v11 )
                  v7 = v8;
                if ( v5 <= v11 )
                  v5 = *(__int16 *)(v8 + 214);
                break;
              case 1:
                v24 = (unsigned int)(26215 * *(char *)(v8 + 50) + 52430) >> 31;
                v25 = v24 + ((26215 * *(char *)(v8 + 50) + 52430) >> 17);
                if ( (__int16)(v24 + ((26215 * *(char *)(v8 + 50) + 52430) >> 17)) < 2 )
                  LOWORD(v25) = 1;
                v25 = (unsigned __int16)v25;
                if ( (unsigned __int16)v25 >= 0x14u )
                  v25 = 20;
                v26 = (unsigned int)(26215 * *(char *)(v8 + 58) + 52430) >> 31;
                v27 = v26 + ((26215 * *(char *)(v8 + 58) + 52430) >> 17);
                if ( (__int16)(v26 + ((26215 * *(char *)(v8 + 58) + 52430) >> 17)) < 2 )
                  LOWORD(v27) = 1;
                v27 = (unsigned __int16)v27;
                if ( (unsigned __int16)v27 >= 0x14u )
                  v27 = 20;
                v28 = v25 + v27;
                v29 = (unsigned int)(26215 * *(char *)(v8 + 59) + 52430) >> 31;
                v30 = v29 + ((26215 * *(char *)(v8 + 59) + 52430) >> 17);
                if ( (__int16)(v29 + ((26215 * *(char *)(v8 + 59) + 52430) >> 17)) < 2 )
                  LOWORD(v30) = 1;
                v30 = (unsigned __int16)v30;
                if ( (unsigned __int16)v30 >= 0x14u )
                  v30 = 20;
                v31 = v28 + v30;
                v32 = (unsigned int)(26215 * *(char *)(v8 + 60) + 52430) >> 31;
                v33 = v32 + ((26215 * *(char *)(v8 + 60) + 52430) >> 17);
                if ( (__int16)(v32 + ((26215 * *(char *)(v8 + 60) + 52430) >> 17)) < 2 )
                  LOWORD(v33) = 1;
                v33 = (unsigned __int16)v33;
                if ( (unsigned __int16)v33 >= 0x14u )
                  v33 = 20;
                v34 = v31 + v33;
                v35 = (unsigned int)(26215 * *(char *)(v8 + 66) + 52430) >> 31;
                v36 = v35 + ((26215 * *(char *)(v8 + 66) + 52430) >> 17);
                if ( (__int16)(v35 + ((26215 * *(char *)(v8 + 66) + 52430) >> 17)) < 2 )
                  LOWORD(v36) = 1;
                v37 = (unsigned __int16)v36;
                if ( (unsigned __int16)v36 >= 0x14u )
                  v37 = 20;
                v38 = v34 + v37;
                v39 = (unsigned int)(26215 * *(char *)(v8 + 65) + 52430) >> 31;
                v40 = v39 + ((26215 * *(char *)(v8 + 65) + 52430) >> 17);
                if ( (__int16)(v39 + ((26215 * *(char *)(v8 + 65) + 52430) >> 17)) < 2 )
                  LOWORD(v40) = 1;
                v41 = (unsigned __int16)v40;
                if ( (unsigned __int16)v40 >= 0x14u )
                  v41 = 20;
                v42 = v38 + v41;
                v43 = (unsigned int)(26215 * *(char *)(v8 + 51) + 52430) >> 31;
                v44 = v43 + ((26215 * *(char *)(v8 + 51) + 52430) >> 17);
                if ( (__int16)(v43 + ((26215 * *(char *)(v8 + 51) + 52430) >> 17)) < 2 )
                  LOWORD(v44) = 1;
                v45 = (unsigned __int16)v44;
                if ( (unsigned __int16)v44 >= 0x14u )
                  v45 = 20;
                v46 = (unsigned int)(26215 * *(char *)(v8 + 61) + 52430) >> 31;
                v47 = v46 + ((26215 * *(char *)(v8 + 61) + 52430) >> 17);
                if ( (__int16)(v46 + ((26215 * *(char *)(v8 + 61) + 52430) >> 17)) < 2 )
                  LOWORD(v47) = 1;
                v47 = (unsigned __int16)v47;
                if ( (unsigned __int16)v47 >= 0x14u )
                  v47 = 20;
                v48 = (unsigned int)(26215 * *(char *)(v8 + 63) + 52430) >> 31;
                v49 = v48 + ((26215 * *(char *)(v8 + 63) + 52430) >> 17);
                if ( (__int16)(v48 + ((26215 * *(char *)(v8 + 63) + 52430) >> 17)) < 2 )
                  LOWORD(v49) = 1;
                v49 = (unsigned __int16)v49;
                if ( (unsigned __int16)v49 >= 0x14u )
                  v49 = 20;
                v50 = (unsigned int)(26215 * *(char *)(v8 + 62) + 52430) >> 31;
                v51 = v50 + ((26215 * *(char *)(v8 + 62) + 52430) >> 17);
                if ( (__int16)(v50 + ((26215 * *(char *)(v8 + 62) + 52430) >> 17)) < 2 )
                  LOWORD(v51) = 1;
                v19 = (unsigned __int16)v51;
                if ( (unsigned __int16)v51 >= 0x14u )
                  v19 = 20;
                v21 = v49 + v47 + v45 + v42 + *(char *)(v8 + 26);
                goto LABEL_82;
              case 2:
                v18 = (unsigned int)(26215 * *(char *)(v8 + 55) + 52430) >> 31;
                v19 = v18 + ((26215 * *(char *)(v8 + 55) + 52430) >> 17);
                if ( (__int16)(v18 + ((26215 * *(char *)(v8 + 55) + 52430) >> 17)) < 2 )
                  LOWORD(v19) = 1;
                v19 = (unsigned __int16)v19;
                if ( (unsigned __int16)v19 >= 0x14u )
                  v19 = 20;
                v20 = (unsigned int)(26215 * *(char *)(v8 + 57) + 52430) >> 31;
                v21 = v20 + ((26215 * *(char *)(v8 + 57) + 52430) >> 17);
                if ( (__int16)(v20 + ((26215 * *(char *)(v8 + 57) + 52430) >> 17)) < 2 )
                  LOWORD(v21) = 1;
                v21 = (unsigned __int16)v21;
                if ( (unsigned __int16)v21 >= 0x14u )
                  v21 = 20;
LABEL_82:
                v23 = v19 + v21;
                goto LABEL_83;
              case 3:
                v22 = *(int *)(*(_QWORD *)(v8 + 8) + 8LL);
                v23 = *(char *)(v22 + v8 + 94)
                    + *(char *)(v22 + v8 + 92)
                    + *(char *)(v22 + v8 + 93)
                    - *(char *)(v22 + v8 + 95)
                    + 21;
LABEL_83:
                if ( v23 > v5 )
                {
                  v7 = v8;
                  v5 = v23;
                }
                break;
              case 4:
                v12 = (unsigned int)(26215 * *(char *)(v8 + 52) + 52430) >> 31;
                v13 = v12 + ((26215 * *(char *)(v8 + 52) + 52430) >> 17);
                if ( (__int16)(v12 + ((26215 * *(char *)(v8 + 52) + 52430) >> 17)) < 2 )
                  LOWORD(v13) = 1;
                v13 = (unsigned __int16)v13;
                if ( (unsigned __int16)v13 >= 0x14u )
                  v13 = 20;
                v14 = (unsigned int)(26215 * *(char *)(v8 + 53) + 52430) >> 31;
                v15 = v14 + ((26215 * *(char *)(v8 + 53) + 52430) >> 17);
                if ( (__int16)(v14 + ((26215 * *(char *)(v8 + 53) + 52430) >> 17)) < 2 )
                  LOWORD(v15) = 1;
                v15 = (unsigned __int16)v15;
                if ( (unsigned __int16)v15 >= 0x14u )
                  v15 = 20;
                v16 = v13 + v15;
                v17 = *(char *)(v8 + 74);
                goto LABEL_91;
              case 5:
                v52 = (unsigned int)(26215 * *(char *)(v8 + 55) + 52430) >> 31;
                v53 = v52 + ((26215 * *(char *)(v8 + 55) + 52430) >> 17);
                if ( (__int16)(v52 + ((26215 * *(char *)(v8 + 55) + 52430) >> 17)) < 2 )
                  LOWORD(v53) = 1;
                v53 = (unsigned __int16)v53;
                if ( (unsigned __int16)v53 >= 0x14u )
                  v53 = 20;
                v16 = v53 + *(char *)(v8 + 28);
                v17 = *(char *)(v8 + 54);
LABEL_91:
                v54 = ((unsigned int)(26215 * v17 + 52430) >> 31) + ((26215 * v17 + 52430) >> 17);
                if ( (__int16)v54 < 2 )
                  LOWORD(v54) = 1;
                v54 = (unsigned __int16)v54;
                if ( (unsigned __int16)v54 >= 0x14u )
                  v54 = 20;
                v55 = v16 + v54;
                if ( v55 > v5 )
                {
                  v7 = v8;
                  v5 = v55;
                }
                break;
              default:
                break;
            }
          }
        }
      }
      if ( v4 == ++v6 )
        goto LABEL_100;
    }
  }
  v7 = 0;
LABEL_100:
  if ( *((_QWORD *)&v62 + 1) == (_QWORD)v62
    || v7 != 0
    || *(_BYTE *)(a1 + 47) != 0
    || (v56 = *(_QWORD *)(a1 + 48)) == 0
    || (*(_BYTE *)(v56 + 353) & 1) == 0 && sub_1408FF650(v56) == 0 )
  {
    v57 = v63;
    if ( (_QWORD)v63 == 0 )
      return v7;
  }
  else
  {
    v57 = v63;
    v7 = *(_QWORD *)v63;
  }
  v58 = v64 - v57;
  if ( v64 - v57 == -1 )
  {
    v58 = *(unsigned int *)(v57 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
LABEL_117:
      MEMORY[0x141948990](v57 - *(unsigned int *)(qword_141ABD470 + 48));
      return v7;
    }
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    goto LABEL_117;
  }
  v59 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v59) >> 3 <= v58 )
    goto LABEL_117;
  v60 = *(_QWORD *)(v59 + 8 * v58);
  if ( v60 == 0 )
    goto LABEL_117;
  MEMORY[0x1419475D8](v60 + 32, v57 - *(unsigned int *)(v60 + 120));
  if ( (*(_BYTE *)(v60 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v60 + 64)) == 0)
    && *(_BYTE *)(v60 + 97) != 0 )
  {
    sub_1412D33C0(v60);
  }
  return v7;
}
