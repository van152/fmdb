__int64 __fastcall sub_140E79030(__int64 a1, char a2, __int64 a3, char a4)
{
  __int64 v4; // rax
  __int64 v7; // r12
  __int64 v8; // rcx
  __int64 v9; // rax
  char v10; // cl
  _BYTE *v11; // rdx
  __int64 result; // rax
  _BYTE *v13; // rax
  bool v14; // r15
  int v15; // ebp
  __int64 v16; // rcx
  __int64 v17; // r10
  __int64 **v18; // rbx
  __int64 **v19; // rdx
  __int64 **v20; // rcx
  __int64 *v21; // rdi
  unsigned int v22; // esi
  char v23; // r8
  __int64 *v24; // rcx
  __int64 v25; // rsi
  __int64 v26; // rbp
  int v27; // edi
  int v28; // ecx
  char v29; // r9
  int v30; // ebp
  __int64 v31; // rcx
  __int64 v32; // r10
  __int64 **v33; // rbx
  __int64 **v34; // rdx
  __int64 **v35; // rcx
  __int64 *v36; // rdi
  unsigned int v37; // esi
  char v38; // r8
  __int64 *v39; // rcx
  __int64 v40; // rsi
  __int64 v41; // rbp
  int v42; // edi
  int v43; // ecx
  __int64 *v44; // rax
  unsigned int v45; // r13d
  __int64 v46; // rcx
  char v47; // bl
  __int64 v48; // rax
  __int64 v49; // rcx
  __int64 v50; // rax
  __int64 v51; // rcx
  char v52; // al
  __int64 v53; // rax
  unsigned __int64 v54; // rbx
  char v55; // r9
  unsigned __int8 v56; // cl
  __int64 *v57; // rcx
  __int64 *v58; // r8
  __int64 v59; // rax
  __int64 v60; // rbp
  __int64 v61; // rbx
  int v62; // eax
  int v63; // ecx
  int v64; // ebp
  int v65; // ebx
  int v66; // ecx
  unsigned int v67; // ecx
  __int64 v68; // rsi
  bool v69; // cl
  __int64 v70; // rdx
  unsigned int v71; // r15d
  __int64 *v72; // rax
  __int64 v73; // rax
  int v74; // eax
  __int64 v75; // rbp
  __int64 *j; // rbx
  __int64 *v77; // rsi
  unsigned int v78; // edx
  __int16 v79; // ax
  __int64 v80; // rcx
  __int64 v81; // rbx
  __int64 v82; // rax
  __int64 *v83; // rcx
  __int64 *v84; // rdx
  int v85; // ebx
  __int64 *v86; // rbp
  unsigned int v87; // edi
  char v88; // bl
  __int64 v89; // rdx
  unsigned int v90; // eax
  __int64 v91; // r8
  unsigned __int64 v92; // r10
  int v93; // ebx
  __int64 v94; // rbp
  __int64 v95; // rdx
  __int64 *v96; // rsi
  __int64 *v97; // rdi
  __int64 *v98; // rbp
  unsigned int v99; // ecx
  int v100; // ecx
  __int64 v101; // rbp
  __int64 v102; // rdx
  __int64 *v103; // rbx
  __int64 *v104; // rdi
  __int64 *v105; // rbp
  unsigned int v106; // esi
  __int16 v107; // si
  char v108; // bl
  __int64 v109; // rax
  __int16 v110; // cx
  int v111; // r8d
  int v112; // edx
  __int64 v113; // rsi
  __int64 *i; // rbx
  __int64 *v115; // rbp
  unsigned int v116; // ecx
  __int64 *v117; // rdx
  __int64 v118; // rdx
  __int64 v119; // [rsp+20h] [rbp-58h]
  __int64 v120; // [rsp+28h] [rbp-50h]

  v4 = *(_QWORD *)(a1 + 216);
  if ( v4 == 0 )
    return 0;
  v7 = a1;
  if ( *(_BYTE *)(a1 + 185) == 0 || (v8 = *(_QWORD *)(v4 + 272)) == 0 )
    v8 = *(_QWORD *)(v4 + 264);
  if ( (_BYTE)word_141B60320 == 0 )
    goto LABEL_17;
  v9 = *(_QWORD *)(*(_QWORD *)(v8 + 368) + 288LL);
  if ( v9 == 0 )
    goto LABEL_17;
  v10 = *(_BYTE *)(v8 + 185);
  if ( v10 != 0 )
  {
    v11 = *(_BYTE **)(v9 + 624);
    if ( v11 == nullptr )
    {
LABEL_17:
      v14 = false;
      goto LABEL_18;
    }
  }
  else
  {
    v11 = *(_BYTE **)(v9 + 624);
  }
  v13 = (_BYTE *)(v9 + 88);
  if ( v10 != 0 )
    v13 = v11;
  if ( v13 == nullptr || *(_BYTE *)(*(_QWORD *)v13 + 68LL) == 0 )
    goto LABEL_17;
  v14 = (v13[522] & 0xFD) == 0;
LABEL_18:
  v15 = 1049072;
  v16 = v7;
  while ( 2 )
  {
    v17 = v16;
    v18 = *(__int64 ***)(v16 + 280);
    v19 = *(__int64 ***)(v16 + 288);
    v20 = v18;
    if ( v18 == v19 )
    {
      v29 = *(_BYTE *)(*(_QWORD *)(v17 + 256) + 299LL);
    }
    else
    {
      while ( 1 )
      {
        v21 = *v20;
        if ( (*v20)[1] == v17 )
        {
          v22 = *((unsigned __int8 *)v21 + 48);
          if ( v22 <= 0x14 )
          {
            if ( _bittest(&v15, v22) )
              break;
          }
        }
        if ( ++v20 == v19 )
          goto LABEL_26;
      }
      v16 = *v21;
      if ( *v21 != 0 )
        continue;
LABEL_26:
      v23 = *(_BYTE *)(*(_QWORD *)(v17 + 256) + 299LL);
      v29 = v23;
      do
      {
        v24 = *v18;
        v25 = **v18;
        if ( v25 != 0 )
        {
          v26 = v24[1];
          if ( v26 != 0 )
          {
            v27 = *((unsigned __int8 *)v24 + 48);
            if ( (unsigned int)(v27 - 4) >= 5 && v27 != 20 )
            {
              v28 = *((_DWORD *)v24 + 7);
              if ( (v28 & 0x400) != 0 && v26 == v17 || (v28 & 0x10000) != 0 && v26 == v17 )
              {
                v23 = *(_BYTE *)(*(_QWORD *)(v25 + 256) + 299LL);
                if ( v23 <= 0 )
                  v23 = 0;
              }
              if ( v23 > v29 )
                v29 = v23;
            }
          }
        }
        ++v18;
      }
      while ( v18 != v19 );
    }
    break;
  }
  if ( v29 > 0 )
  {
    v30 = 1049072;
    v31 = v7;
    while ( 2 )
    {
      v32 = v31;
      v33 = *(__int64 ***)(v31 + 280);
      v34 = *(__int64 ***)(v31 + 288);
      v35 = v33;
      if ( v33 == v34 )
      {
        v55 = *(_BYTE *)(*(_QWORD *)(v32 + 256) + 299LL);
      }
      else
      {
        while ( 1 )
        {
          v36 = *v35;
          if ( (*v35)[1] == v32 )
          {
            v37 = *((unsigned __int8 *)v36 + 48);
            if ( v37 <= 0x14 )
            {
              if ( _bittest(&v30, v37) )
                break;
            }
          }
          if ( ++v35 == v34 )
            goto LABEL_49;
        }
        v31 = *v36;
        if ( *v36 != 0 )
          continue;
LABEL_49:
        v38 = *(_BYTE *)(*(_QWORD *)(v32 + 256) + 299LL);
        v55 = v38;
        do
        {
          v39 = *v33;
          v40 = **v33;
          if ( v40 != 0 )
          {
            v41 = v39[1];
            if ( v41 != 0 )
            {
              v42 = *((unsigned __int8 *)v39 + 48);
              if ( (unsigned int)(v42 - 4) >= 5 && v42 != 20 )
              {
                v43 = *((_DWORD *)v39 + 7);
                if ( (v43 & 0x400) != 0 && v41 == v32 || (v43 & 0x10000) != 0 && v41 == v32 )
                {
                  v38 = *(_BYTE *)(*(_QWORD *)(v40 + 256) + 299LL);
                  if ( v38 <= 0 )
                    v38 = 0;
                }
                if ( v38 > v55 )
                  v55 = v38;
              }
            }
          }
          ++v33;
        }
        while ( v33 != v34 );
      }
      break;
    }
    v56 = 0;
    if ( v55 > 0 )
      v56 = v55;
    v45 = v56;
    goto LABEL_82;
  }
  v44 = *(__int64 **)(v7 + 24);
  v45 = 0;
  if ( v44 != *(__int64 **)(v7 + 32) )
  {
    v46 = *v44;
    if ( *v44 != 0 )
    {
      if ( *(_BYTE *)(v46 + 40) != 0 )
      {
        v47 = a2;
        v48 = sub_1411A41D0();
        if ( v48 == 0 )
          goto LABEL_78;
      }
      else
      {
        v47 = a2;
        v48 = *(_QWORD *)(v46 + 128);
        if ( v48 == 0 )
          goto LABEL_78;
      }
      v49 = v48 + *(int *)(*(_QWORD *)(v48 + 8) + 4LL) + 8;
      v50 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v49 + 1760LL))(v49);
      if ( v50 != 0 )
      {
        a2 = v47;
        if ( *(_BYTE *)(v50 + 1068) == 0 )
        {
          v51 = *(_QWORD *)(v50 + 944);
          if ( v51 != 0 )
          {
            v52 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v51 + 48LL))(v51);
            a2 = v47;
            if ( v52 == 0 )
            {
              if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) == 0 )
              {
                sub_141751038();
                a2 = v47;
              }
              v53 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex);
              v54 = *(_QWORD *)(v53 + 328);
              *(_QWORD *)(v53 + 328) = *(_QWORD *)(v53 + 336) + 0x5851F42D4C957F2DLL * v54;
              v45 = 25;
              if ( (100 * (unsigned __int64)(unsigned int)__ROR4__((v54 >> 27) ^ (v54 >> 45), v54 >> 59)) >> 32 != 0 )
                v45 = 0;
            }
          }
        }
        goto LABEL_82;
      }
LABEL_78:
      a2 = v47;
    }
  }
LABEL_82:
  v57 = *(__int64 **)(v7 + 24);
  v58 = *(__int64 **)(v7 + 32);
  if ( v57 == v58 )
    goto LABEL_100;
  v59 = *v57;
  if ( *v57 == 0 )
    goto LABEL_100;
  v60 = *(_QWORD *)(v59 + 48);
  if ( v60 != 0 )
    v60 = *(_QWORD *)(v59 + 80);
  v61 = *(_QWORD *)(v59 + 88);
  if ( v61 == 0 )
    v61 = *(_QWORD *)(v59 + 80);
  if ( v60 != 0 && v61 != 0 && *(_BYTE *)(v60 + 418) > *(_BYTE *)(v61 + 418) )
    v61 = v60;
  if ( v61 != 0 && a2 != 0 && a4 != 0 )
  {
    v62 = 5243 * *(__int16 *)(v59 + 168);
    v63 = ((unsigned int)v62 >> 31) + (v62 >> 18);
    v64 = *(__int16 *)(v61 + 384);
    v65 = v64 + v63 + 3;
    v66 = v64 + v63;
    if ( v66 >= 0 )
      v65 = v66;
    v67 = (int)((v65 >> 2) + 2 * (((unsigned int)v62 >> 31) + (v62 >> 19) + v45)) / 3;
    result = 85;
    if ( (__int16)v67 < 85 )
      return v67;
  }
  else
  {
LABEL_100:
    if ( a2 != 0 )
    {
      v68 = *(_QWORD *)(v7 + 216);
      v69 = v14;
      if ( v68 != 0 )
      {
        if ( *(_BYTE *)(v7 + 185) == 0 || (v70 = *(_QWORD *)(v68 + 272)) == 0 )
          v70 = *(_QWORD *)(v68 + 264);
        LOWORD(v71) = *(_WORD *)(v70 + 1932);
        v120 = v70;
        if ( (__int16)v71 <= 0 )
        {
          v72 = *(__int64 **)(v70 + 24);
          LOWORD(v71) = 30;
          if ( v72 != *(__int64 **)(v70 + 32) )
          {
            v73 = *v72;
            if ( v73 != 0 )
              v71 = ((unsigned int)(5243 * *(__int16 *)(v73 + 168)) >> 31) + ((5243 * *(__int16 *)(v73 + 168)) >> 18);
          }
        }
      }
      else
      {
        LOWORD(v71) = 10;
        v120 = 0;
      }
      v81 = v7;
      if ( v69 )
        goto LABEL_174;
      v119 = *(_QWORD *)(v7 + 216);
      if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) == 0 )
      {
        v88 = a2;
        sub_141751038();
        a2 = v88;
      }
      v89 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex);
      v90 = __ROR4__((*(_QWORD *)(v89 + 328) >> 27) ^ (*(_QWORD *)(v89 + 328) >> 45), *(_QWORD *)(v89 + 328) >> 59);
      v91 = *(_QWORD *)(v89 + 336);
      v92 = v91 + 0x5851F42D4C957F2DLL * *(_QWORD *)(v89 + 328);
      *(_QWORD *)(v89 + 328) = v92;
      v93 = 1049072;
      v94 = v7;
LABEL_133:
      v95 = v94;
      v96 = *(__int64 **)(v94 + 280);
      v97 = *(__int64 **)(v94 + 288);
      while ( v96 != v97 )
      {
        v98 = (__int64 *)*v96;
        if ( *(_QWORD *)(*v96 + 8) == v95 )
        {
          v99 = *((unsigned __int8 *)v98 + 48);
          if ( v99 <= 0x14 )
          {
            if ( _bittest(&v93, v99) )
            {
              v94 = *v98;
              if ( v94 != 0 )
                goto LABEL_133;
              break;
            }
          }
        }
        ++v96;
      }
      v81 = v7;
      v68 = v119;
      if ( (__int16)v71 < 100
        || (v81 = v7, (int)((40 * (unsigned __int64)v90) >> 32) >= *(char *)(*(_QWORD *)(v95 + 256) + 301LL)) )
      {
LABEL_174:
        do
        {
          v82 = v81;
          v83 = *(__int64 **)(v81 + 280);
          v84 = *(__int64 **)(v81 + 288);
          if ( v83 == v84 )
            break;
          v85 = 1049072;
          while ( 1 )
          {
            v86 = (__int64 *)*v83;
            if ( *(_QWORD *)(*v83 + 8) == v82 )
            {
              v87 = *((unsigned __int8 *)v86 + 48);
              if ( v87 <= 0x14 )
              {
                if ( _bittest(&v85, v87) )
                  break;
              }
            }
            if ( ++v83 == v84 )
              goto LABEL_129;
          }
          v81 = *v86;
        }
        while ( *v86 != 0 );
LABEL_129:
        v79 = *(char *)(*(_QWORD *)(v82 + 256) + 300LL);
      }
      else
      {
        v100 = 1049072;
        v101 = v7;
LABEL_143:
        v102 = v101;
        v103 = *(__int64 **)(v101 + 280);
        v104 = *(__int64 **)(v101 + 288);
        while ( v103 != v104 )
        {
          v105 = (__int64 *)*v103;
          if ( *(_QWORD *)(*v103 + 8) == v102 )
          {
            v106 = *((unsigned __int8 *)v105 + 48);
            if ( v106 <= 0x14 )
            {
              if ( _bittest(&v100, v106) )
              {
                v101 = *v105;
                if ( v101 != 0 )
                  goto LABEL_143;
                break;
              }
            }
          }
          ++v103;
        }
        v107 = *(char *)(*(_QWORD *)(v102 + 256) + 300LL);
        if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) == 0 )
        {
          v108 = a2;
          sub_141751038();
          a2 = v108;
          v109 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex);
          v92 = *(_QWORD *)(v109 + 328);
          v91 = *(_QWORD *)(v109 + 336);
        }
        *(_QWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 328LL) = v91 + 0x5851F42D4C957F2DLL * v92;
        v79 = v107
            + (((unsigned __int64)(unsigned int)__ROR4__((v92 >> 27) ^ (v92 >> 45), v92 >> 59) * ((char)v107 / 2)) >> 32);
        v68 = v119;
      }
      if ( a3 != 0 && v68 != a3 )
      {
        v110 = *(_WORD *)(v120 + 1932);
        if ( v110 <= 0 )
        {
          v117 = *(__int64 **)(v120 + 24);
          v110 = 30;
          if ( v117 != *(__int64 **)(v120 + 32) )
          {
            v118 = *v117;
            if ( v118 != 0 )
              v110 = *(__int16 *)(v118 + 168) / 50;
          }
        }
        v111 = v110;
        v112 = 1049072;
LABEL_157:
        v113 = v7;
        for ( i = *(__int64 **)(v7 + 280); i != *(__int64 **)(v7 + 288); ++i )
        {
          v115 = (__int64 *)*i;
          if ( *(_QWORD *)(*i + 8) == v7 )
          {
            v116 = *((unsigned __int8 *)v115 + 48);
            if ( v116 <= 0x14 )
            {
              if ( _bittest(&v112, v116) )
              {
                v7 = *v115;
                if ( *v115 != 0 )
                  goto LABEL_157;
                break;
              }
            }
          }
        }
        if ( (__int16)(v111 * *(char *)(*(_QWORD *)(v113 + 256) + 301LL) / 20) > (__int16)v71 )
          LOWORD(v71) = v111 * *(char *)(*(_QWORD *)(v113 + 256) + 301LL) / 20;
      }
    }
    else
    {
      v74 = 1049072;
LABEL_110:
      v75 = v7;
      for ( j = *(__int64 **)(v7 + 280); j != *(__int64 **)(v7 + 288); ++j )
      {
        v77 = (__int64 *)*j;
        if ( *(_QWORD *)(*j + 8) == v7 )
        {
          v78 = *((unsigned __int8 *)v77 + 48);
          if ( v78 <= 0x14 )
          {
            if ( _bittest(&v74, v78) )
            {
              v7 = *v77;
              if ( *v77 != 0 )
                goto LABEL_110;
              break;
            }
          }
        }
      }
      v79 = 4 * *(char *)(*(_QWORD *)(v75 + 256) + 300LL);
      LOWORD(v71) = 15;
      if ( v57 != v58 )
      {
        v80 = *v57;
        if ( v80 != 0 )
          LOWORD(v71) = *(__int16 *)(v80 + 168) / 100;
      }
    }
    if ( a2 != 0 )
      return (unsigned int)(int)(float)((float)((float)(v45 / 5)
                                              + (float)((float)((float)(__int16)v71
                                                              * (float)((float)v79 / MEMORY[0x141775564]))
                                                      * MEMORY[0x141764680]))
                                      * MEMORY[0x141774718]);
    else
      return (v79 + v45 + (__int16)v71 + ((v79 + v45 + (__int16)v71) >> 31)) >> 1;
  }
  return result;
}
