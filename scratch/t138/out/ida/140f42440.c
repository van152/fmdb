__int64 __fastcall sub_140F42440(__int64 *a1, __int64 a2, __int64 a3)
{
  __int64 *v5; // rsi
  __int64 v6; // rcx
  __int64 v8; // r9
  void (__fastcall ***v9)(_QWORD, __int64); // rcx
  __int64 *v10; // rdi
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rax
  unsigned __int64 v14; // rax
  __int64 v15; // r15
  __int64 v16; // r12
  _QWORD *v17; // r12
  __int64 v18; // r15
  __int64 v19; // r14
  bool v20; // al
  _QWORD *v21; // rdx
  __int64 v22; // rdi
  _QWORD *v23; // rbx
  _QWORD **v24; // r13
  _QWORD *v25; // rcx
  unsigned __int64 *v26; // rsi
  _QWORD **v27; // rdi
  _QWORD *v28; // r15
  __int64 v29; // rsi
  __int64 *v30; // rbx
  void (__fastcall *v31)(__int64); // r15
  __int64 v32; // rcx
  _QWORD *v33; // rsi
  __int64 v34; // rdi
  unsigned __int64 v35; // rbx
  unsigned __int64 v36; // rcx
  __int64 v37; // rdx
  __int64 v38; // rdi
  bool v39; // al
  _QWORD *v40; // rbx
  __int64 v41; // rdi
  bool v42; // al
  __int64 v43; // rbx
  bool v44; // al
  void (__fastcall ***v45)(_QWORD, __int64); // rcx
  __int64 *v46; // rax
  __int16 v47; // di
  __int64 v48; // r9
  void (__fastcall ***v49)(_QWORD, __int64); // rcx
  void (__fastcall ***v50)(_QWORD, __int64); // rcx
  int v51; // r13d
  unsigned __int64 v52; // r14
  unsigned __int64 v53; // rdi
  unsigned __int64 v54; // rbx
  bool v55; // zf
  __int64 v56; // rcx
  __int64 v57; // rcx
  __int64 v58; // r15
  char *v59; // rax
  char *v60; // rbx
  __int64 *v61; // r15
  __int64 v62; // rdx
  __int64 **v63; // r15
  __int64 *v64; // rdi
  __int64 *v65; // rbx
  __int64 v66; // r14
  unsigned __int64 v67; // rcx
  __int64 v68; // rdx
  __int64 v69; // rbx
  bool v70; // al
  __int64 v71; // rdi
  bool v72; // al
  volatile signed __int32 *v73; // rcx
  __int64 v74; // rdi
  _QWORD *v75; // rsi
  _QWORD *v76; // rdi
  _QWORD v77[2]; // [rsp+48h] [rbp-38h] BYREF
  char v78[16]; // [rsp+58h] [rbp-28h] BYREF
  _QWORD v79[6]; // [rsp+68h] [rbp-18h] BYREF
  __int64 v80; // [rsp+98h] [rbp+18h]
  _QWORD *v81; // [rsp+C0h] [rbp+40h]
  _QWORD *v82; // [rsp+C8h] [rbp+48h]
  __int16 v83; // [rsp+E8h] [rbp+68h]
  char v84; // [rsp+EBh] [rbp+6Bh]
  __int64 v85; // [rsp+F0h] [rbp+70h] BYREF
  __int64 *v86; // [rsp+F8h] [rbp+78h]
  unsigned __int64 v87; // [rsp+100h] [rbp+80h]
  volatile signed __int32 *v88; // [rsp+108h] [rbp+88h] BYREF
  __int64 v89; // [rsp+110h] [rbp+90h] BYREF
  __int64 v90; // [rsp+118h] [rbp+98h]
  __int64 v91; // [rsp+120h] [rbp+A0h] BYREF
  _QWORD *v92; // [rsp+128h] [rbp+A8h]
  __int64 v93; // [rsp+130h] [rbp+B0h]

  v93 = -2;
  v5 = a1;
  v6 = a1[1];
  if ( v6 != 0 )
    return sub_140FBC8F0(a1: v6, a2, a3);
  v8 = v5[2];
  if ( v8 != 0 )
  {
    v77[0] = 0x80100004E554C4CLL;
    sub_1407D0F70(a1: (unsigned int)v77, a2: (unsigned int)&v91, a3: a2, a4: v8 + 72, a5: a3, a6: 1, a7: 0, 0);
    v9 = (void (__fastcall ***)(_QWORD, __int64))v91;
    if ( v91 != 0 )
    {
      if ( _InterlockedDecrement((volatile signed __int32 *)(v91 + 8)) == 0 )
        (**v9)(a1: v9, a2: 1);
      if ( (unsigned __int8)sub_140FBC8F0(a1: v5[2], a2, a3) != 0 )
      {
        v10 = (__int64 *)v5[2];
        v11 = *v10;
        v12 = v10[1];
        LODWORD(v77[0]) = -1;
        v13 = v12 - v11;
        if ( v13 == 0 )
        {
LABEL_88:
          sub_140FB5900(a1: v10);
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
            }
          }
          if ( byte_141B59A9C != 0
            && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0x341
            && (v43 = *(_QWORD *)(qword_141B59A80 + 832)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v43 + 32, a2: (char *)v10 - *(unsigned int *)(v43 + 120));
            v44 = *(_BYTE *)(v43 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v43 + 64)) != 0;
            if ( !v44 && *(_BYTE *)(v43 + 97) != 0 )
              sub_1412D33C0(a1: v43);
          }
          else
          {
            MEMORY[0x141948990](a1: (char *)v10 - (unsigned int)dword_141B59A98);
          }
          goto LABEL_95;
        }
        v14 = v13 >> 3;
        v15 = 1;
        if ( v14 >= 2 )
          v15 = v14;
        v16 = 0;
        v90 = v15;
        v86 = v5;
        do
        {
          LODWORD(v77[0]) = v16;
          if ( (int)v16 < 0 )
            goto LABEL_21;
          v21 = (_QWORD *)v5[2];
          if ( (__int64)(v21[1] - *v21) >> 3 <= (unsigned __int64)(unsigned int)v16 )
            goto LABEL_21;
          v22 = *(_QWORD *)(*v21 + 8LL * (unsigned int)v16);
          if ( v22 == 0 )
            goto LABEL_21;
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
              v15 = v90;
            }
          }
          v23 = (_QWORD *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
          *v23 = 0;
          v23[1] = 0;
          v23[2] = 0;
          v92 = v23;
          if ( qword_141ABD470 == 0 )
          {
            if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(a1: &dword_141B59AA8);
              if ( dword_141B59AA8 == -1 )
              {
                sub_1407E3E70(a1: &unk_141B59A68);
                sub_141751048(a1: sub_1407E4B20);
                sub_141750EA0(a1: &dword_141B59AA8);
                v15 = v90;
                v23 = v92;
              }
            }
            qword_141ABD470 = (__int64)&unk_141B59A68;
          }
          v23[2] = 0;
          v23[1] = 0;
          *v23 = 0;
          sub_140FBE6C0(a1: v23, a2: v22);
          v24 = (_QWORD **)v23[1];
          if ( v24 != (_QWORD **)*v23 )
          {
            v25 = (_QWORD *)*v5;
            v26 = v92;
            sub_140FBDB40(a1: v25, a2: v77);
            v24 = (_QWORD **)v26[1];
            v87 = *v26;
            v27 = (_QWORD **)v87;
            if ( (_QWORD **)v87 != v24 )
            {
              do
              {
                v28 = *v27;
                if ( *v27 != nullptr )
                {
                  if ( dword_141B5F2D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                     + (unsigned int)TlsIndex)
                                                   + 4LL) )
                  {
                    sub_141750E08(a1: &dword_141B5F2D0);
                    if ( dword_141B5F2D0 == -1 )
                    {
                      sub_1407E53D0(
                        a1: (unsigned int)&unk_141B5F280,
                        a2: 1100122401,
                        a3: 128,
                        a4: 64,
                        a5: 0,
                        a6: 0,
                        a7: 128,
                        a8: 4096);
                      sub_141751048(a1: sub_140FB3BD0);
                      sub_141750EA0(a1: &dword_141B5F2D0);
                    }
                  }
                  *v28 = qword_141B5F2A8;
                  qword_141B5F2A8 = (__int64)v28;
                  LODWORD(qword_141B5F2B0) = qword_141B5F2B0 + 1;
                  if ( --HIDWORD(qword_141B5F2B0) == 0 && byte_141B5F2C9 != 0 )
                  {
                    v29 = qword_141B5F298;
                    v30 = (__int64 *)qword_141B5F290;
                    v31 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
                    if ( qword_141B5F290 != qword_141B5F298 )
                    {
                      do
                      {
                        v32 = *v30;
                        if ( (dword_141B5F288 & 0xFFF000u) < 0x2001 )
                          v31(a1: v32);
                        else
                          MEMORY[0x141948960](a1: v32);
                        ++v30;
                      }
                      while ( v30 != (__int64 *)v29 );
                      if ( qword_141B5F290 != qword_141B5F298 )
                        qword_141B5F298 = qword_141B5F290;
                    }
                    qword_141B5F2B0 = 0;
                    qword_141B5F2A8 = 0;
                  }
                }
                ++v27;
              }
              while ( v27 != v24 );
              v33 = v92;
              v34 = v92[1] - (_QWORD)v24;
              v35 = v87;
              sub_141758A00(a1: v87, a2: v24, a3: v34);
              v33[1] = v35 + v34;
              v24 = (_QWORD **)*v33;
            }
            v5 = v86;
            v15 = v90;
          }
          if ( v24 != nullptr )
          {
            v36 = v92[2] - (_QWORD)v24;
            if ( v36 == -1 )
            {
              v36 = *(unsigned int *)((char *)v24 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_59;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_59;
            }
            v37 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v37) >> 3 > v36 )
            {
              v38 = *(_QWORD *)(v37 + 8 * v36);
              if ( v38 != 0 )
              {
                MEMORY[0x1419475D8](a1: v38 + 32, a2: (char *)v24 - *(unsigned int *)(v38 + 120));
                v39 = *(_BYTE *)(v38 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 64)) != 0;
                v40 = v92;
                if ( !v39 && *(_BYTE *)(v38 + 97) != 0 )
                  sub_1412D33C0(a1: v38);
                goto LABEL_60;
              }
            }
LABEL_59:
            MEMORY[0x141948990](a1: (char *)v24 - *(unsigned int *)(qword_141ABD470 + 48));
            v40 = v92;
LABEL_60:
            v40[2] = 0;
            v40[1] = 0;
            *v40 = 0;
          }
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
              v15 = v90;
            }
          }
          if ( byte_141B59A9C != 0
            && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0xC1
            && (v41 = *(_QWORD *)(qword_141B59A80 + 192)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v41 + 32, a2: (char *)v92 - *(unsigned int *)(v41 + 120));
            v42 = *(_BYTE *)(v41 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v41 + 64)) != 0;
            if ( !v42 && *(_BYTE *)(v41 + 97) != 0 )
              sub_1412D33C0(a1: v41);
          }
          else
          {
            MEMORY[0x141948990](a1: (char *)v92 - (unsigned int)dword_141B59A98);
          }
LABEL_21:
          ++v16;
        }
        while ( v16 != v15 );
        v10 = (__int64 *)v5[2];
        if ( v10 != nullptr )
          goto LABEL_88;
LABEL_95:
        v5[2] = 0;
        LOBYTE(v5) = 1;
        return (unsigned int)v5;
      }
    }
  }
  v17 = (_QWORD *)*v5;
  if ( *v5 == 0 )
  {
    LODWORD(v5) = 0;
    return (unsigned int)v5;
  }
  v18 = v5[2];
  if ( v18 != 0 )
  {
    sub_140FB5900(a1: v5[2]);
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    if ( byte_141B59A9C != 0
      && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0x341
      && (v19 = *(_QWORD *)(qword_141B59A80 + 832)) != 0 )
    {
      MEMORY[0x1419475D8](a1: v19 + 32, a2: v18 - *(unsigned int *)(v19 + 120));
      v20 = *(_BYTE *)(v19 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 64)) != 0;
      if ( !v20 && *(_BYTE *)(v19 + 97) != 0 )
        sub_1412D33C0(a1: v19);
    }
    else
    {
      MEMORY[0x141948990](a1: v18 - (unsigned int)dword_141B59A98);
    }
    v17 = (_QWORD *)*v5;
  }
  v5[2] = 0;
  v5 = v77;
  sub_14120E760(a1: v77, a2: v17);
  if ( (unsigned __int8)sub_14120F520(a1: v77, a2, a3) != 0 )
  {
    if ( v84 != 0 )
    {
      sub_140FBC310(a1: v17, a2: v77);
LABEL_183:
      LOBYTE(v5) = 1;
LABEL_189:
      sub_140FB5070(a1: v77);
      return (unsigned int)v5;
    }
    if ( v82 != v81 )
    {
      v79[0] = qword_141B61FD0;
      (*(void (__fastcall **)(_QWORD, __int64 *, _QWORD *, _QWORD *))(*(_QWORD *)*v17 + 208LL))(
        a1: *v17,
        a2: &v91,
        a3: v17 + 2,
        a4: v17 + 4);
      if ( v91 == 0 )
        goto LABEL_103;
      (*(void (__fastcall **)(__int64, volatile signed __int32 **, _QWORD *, _QWORD *))(*(_QWORD *)v91 + 128LL))(
        a1: v91,
        a2: &v88,
        a3: v17 + 2,
        a4: v79);
      v45 = (void (__fastcall ***)(_QWORD, __int64))v91;
      if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 + 8)) == 0 )
        (**v45)(a1: v45, a2: 1);
      if ( (_DWORD)v88 != 0 )
      {
LABEL_103:
        if ( (qword_141B61FF0 & 0x100000000LL) != 0 && (int)qword_141B61FF0 <= 1 )
        {
          v46 = &qword_141B61FD8;
          while ( 1 )
          {
            v46 = (__int64 *)v46[2];
            if ( v46 == nullptr || *v46 == 0 )
              break;
            if ( (*((_BYTE *)v46 + 28) & 1) == 0 || *((int *)v46 + 6) > 1 )
              goto LABEL_187;
          }
          v74 = sub_1407E2C90(a1: 2160);
          sub_1407E2EB0(a1: v74, a2: 1099980086, a3: 207, a4: 1100077645, a5: 0, a6: 1);
          sub_1407E0010(a1: v74, a2: 0x141941D5ELL);
          sub_14080CDB0(a1: v74, a2: v17 + 2);
          if ( (sub_1407E0380(a1: &qword_141B61FD8, a2: v74) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
            __debugbreak();
        }
LABEL_187:
        v75 = v81;
        v76 = v82;
        if ( v81 != v82 )
        {
          do
          {
            if ( *v75 != 0 )
            {
              sub_1407E6420(a1: qword_141ABE200, a2: *v75, a3: v75[2] - *v75);
              v75[2] = 0;
              v75[1] = 0;
              *v75 = 0;
            }
            v75 += 3;
          }
          while ( v75 != v76 );
          v82 = v81;
          LODWORD(v5) = 0;
          goto LABEL_189;
        }
        goto LABEL_188;
      }
      (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, char *, _QWORD *))(*(_QWORD *)*v17 + 208LL))(
        a1: *v17,
        a2: &v88,
        a3: v78,
        a4: v79);
      v47 = v83;
      v5 = &v85;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v88 + 168LL))(a1: v88, a2: &v85);
      v91 = 0x80100004E554C4CLL;
      sub_1407D0D80(a1: (unsigned int)&v91, a2: (unsigned int)&v89, a3: (unsigned int)&v85, a4: 1314212940, a5: v47);
      v49 = (void (__fastcall ***)(_QWORD, __int64))v80;
      if ( v80 == v89 )
      {
        if ( v80 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v80 + 8)) == 0 )
          (**v49)(a1: v49, a2: 1);
      }
      else
      {
        if ( v80 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v80 + 8)) == 0 )
          (**v49)(a1: v49, a2: 1);
        v80 = v89;
        v89 = 0;
      }
      v50 = (void (__fastcall ***)(_QWORD, __int64))v85;
      if ( v85 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v85 + 8)) == 0 )
        (**v50)(a1: v50, a2: 1);
      LODWORD(v92) = -1431655765 * ((unsigned __int64)((char *)v82 - (char *)v81) >> 3);
      if ( (int)v92 > 0 )
      {
        v51 = 0;
        do
        {
          LODWORD(v89) = v51;
          LOBYTE(v48) = 1;
          sub_140FBEC40(a1: v77, a2: &v91, a3: &v89, a4: v48);
          if ( v91 != 0 )
          {
            sub_140FBDB40(a1: v17, a2: &v89);
          }
          else
          {
            v5 = (__int64 *)v17[6];
            if ( v5 == (__int64 *)v17[7] )
            {
              v52 = ((__int64)v5 - v17[5]) >> 2;
              v53 = v52 + (v52 >> 1);
              v87 = v52 + 1;
              if ( v53 <= v52 + 1 )
                v53 = v52 + 1;
              if ( v52 > 0x3FFFFFFFFFFFFFFFLL - (v52 >> 1) )
                v53 = 0x3FFFFFFFFFFFFFFFLL;
              v54 = 4 * v53;
              v55 = *(_BYTE *)(qword_141ABE200 + 52) == 0;
              v90 = 4 * v53;
              if ( v55
                || (v56 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v56) >> 3 <= v54)
                || (v57 = *(_QWORD *)(v56 + 32 * v53)) == 0 )
              {
                v58 = *(unsigned int *)(qword_141ABE200 + 48);
                v59 = (char *)sub_141601260(a1: (unsigned int)(v58 + v54), a2: 4096);
              }
              else
              {
                v58 = *(unsigned int *)(v57 + 88);
                v59 = (char *)sub_1407E58C0(a1: v57, a2: *(unsigned int *)(v57 + 80));
              }
              v60 = v59;
              if ( v58 != 0 )
              {
                *(_DWORD *)v59 = v90;
                v60 = &v59[v58];
              }
              *(_DWORD *)&v60[4 * v52] = v51;
              v61 = (__int64 *)v17[6];
              sub_141758A00(a1: v60, a2: v17[5], a3: (char *)v5 - v17[5]);
              if ( v61 != v5 )
                sub_141758A00(a1: &v60[4 * v52 + 4], a2: v5, a3: v17[6] - (_QWORD)v5);
              v62 = v17[5];
              if ( v62 != 0 )
                sub_1407E6420(a1: qword_141ABE200, a2: v62, a3: v17[7] - v62);
              v17[5] = v60;
              v17[6] = &v60[4 * v87];
              v17[7] = &v60[4 * v53];
            }
            else
            {
              *(_DWORD *)v5 = v51;
              v17[6] += 4LL;
            }
          }
          v63 = (__int64 **)v91;
          if ( v91 != 0 )
          {
            v5 = *(__int64 **)v91;
            v64 = *(__int64 **)(v91 + 8);
            v65 = *(__int64 **)v91;
            if ( *(__int64 **)v91 != v64 )
            {
              do
              {
                if ( *v65 != 0 )
                  sub_140F6BAB0();
                ++v65;
              }
              while ( v65 != v64 );
              v66 = (char *)v63[1] - (char *)v64;
              sub_141758A00(a1: v5, a2: v64, a3: v66);
              v63[1] = (__int64 *)((char *)v5 + v66);
              v64 = *v63;
            }
            if ( v64 != nullptr )
            {
              v67 = (char *)v63[2] - (char *)v64;
              if ( v67 == -1 )
                v67 = *(unsigned int *)((char *)v64 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v68 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v68) >> 3 > v67)
                && (v69 = *(_QWORD *)(v68 + 8 * v67)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v69 + 32, a2: (char *)v64 - *(unsigned int *)(v69 + 120));
                v70 = *(_BYTE *)(v69 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v69 + 64)) != 0;
                if ( !v70 && *(_BYTE *)(v69 + 97) != 0 )
                  sub_1412D33C0(a1: v69);
              }
              else
              {
                MEMORY[0x141948990](a1: (char *)v64 - *(unsigned int *)(qword_141ABD470 + 48));
              }
              v63[2] = nullptr;
              v63[1] = nullptr;
              *v63 = nullptr;
            }
            if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(a1: &dword_141B59AA8);
              if ( dword_141B59AA8 == -1 )
              {
                sub_1407E3E70(a1: &unk_141B59A68);
                sub_141751048(a1: sub_1407E4B20);
                sub_141750EA0(a1: &dword_141B59AA8);
              }
            }
            if ( byte_141B59A9C != 0
              && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0xC1
              && (v71 = *(_QWORD *)(qword_141B59A80 + 192)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v71 + 32, a2: (char *)v63 - *(unsigned int *)(v71 + 120));
              v72 = *(_BYTE *)(v71 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 64)) != 0;
              if ( !v72 && *(_BYTE *)(v71 + 97) != 0 )
                sub_1412D33C0(a1: v71);
            }
            else
            {
              MEMORY[0x141948990](a1: (char *)v63 - (unsigned int)dword_141B59A98);
            }
          }
          ++v51;
        }
        while ( v51 != (_DWORD)v92 );
      }
      v73 = v88;
      if ( v88 != nullptr && _InterlockedDecrement(v88 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v73)(a1: v73, a2: 1);
    }
    sub_14120F2B0(a1: v77);
    goto LABEL_183;
  }
LABEL_188:
  LODWORD(v5) = 0;
  goto LABEL_189;
}
