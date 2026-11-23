void __fastcall sub_140F7AAC0(__int64 a1, __int64 a2, __int64 a3, char a4)
{
  __int64 **v7; // rax
  __int64 *v8; // rsi
  __int64 *v9; // rbx
  __int64 v10; // rax
  __int64 v11; // rcx
  volatile signed __int32 *v12; // rdi
  volatile signed __int32 *v13; // rdi
  __int64 v14; // rax
  int v15; // r13d
  __int64 v16; // rcx
  volatile signed __int32 *v17; // rbx
  __int64 v18; // rbp
  __int64 v19; // r8
  int v20; // eax
  char v21; // bl
  void (__fastcall ***v22)(_QWORD, __int64); // rcx
  __int64 v23; // r12
  int v24; // esi
  __int64 *v25; // rbx
  __int64 v26; // r13
  __int64 v27; // rdx
  __int64 *v28; // rax
  __int64 *v29; // rdx
  __int64 *v30; // rcx
  __int64 *v31; // rdi
  __int64 v32; // rbx
  __int64 v33; // rdi
  __int64 v34; // rdx
  __int64 *v35; // rax
  __int64 *v36; // rdx
  __int64 *v37; // rcx
  __int64 *v38; // rsi
  __int64 v39; // rbx
  __int64 v40; // rdi
  __int64 v41; // rdx
  __int64 *v42; // rax
  __int64 *v43; // rdx
  __int64 *v44; // rcx
  __int64 *v45; // rsi
  __int64 v46; // rcx
  __int64 v47; // rax
  __int64 v48; // r8
  char v49; // si
  volatile signed __int32 *v50; // rcx
  __int64 v51; // rcx
  void (__fastcall ***v52)(_QWORD, __int64); // rcx
  int v53; // [rsp+30h] [rbp-98h]
  char v54; // [rsp+47h] [rbp-81h] BYREF
  __int64 v55; // [rsp+48h] [rbp-80h] BYREF
  char v56; // [rsp+57h] [rbp-71h] BYREF
  volatile signed __int32 *v57; // [rsp+58h] [rbp-70h] BYREF
  __int64 v58; // [rsp+60h] [rbp-68h] BYREF
  unsigned int v59; // [rsp+68h] [rbp-60h] BYREF
  __int64 v60; // [rsp+70h] [rbp-58h] BYREF
  __int64 v61; // [rsp+78h] [rbp-50h]
  __int64 v62[9]; // [rsp+80h] [rbp-48h] BYREF

  if ( (_BYTE)a3 != 0 )
  {
    v7 = *(__int64 ***)(a1 + 128);
    v8 = *v7;
    v9 = v7[1];
    if ( *v7 != v9 )
    {
      while ( 1 )
      {
        v10 = *v8;
        LOBYTE(v58) = 0;
        v55 = v10;
        v11 = *(_QWORD *)(a2 + 56);
        if ( v11 == 0 )
          break;
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v11 + 16LL))(a1: v11, a2: &v55, a3: &v58);
        if ( ++v8 == v9 )
          goto LABEL_5;
      }
LABEL_101:
      sub_141758410();
      goto LABEL_102;
    }
  }
LABEL_5:
  if ( *(_BYTE *)(a1 + 89) != 0 || a4 == 0 )
    return;
  v62[0] = 0;
  LOBYTE(a3) = 1;
  sub_140F45A00(a1: &qword_141B5FDA8, a2: &v58, a3, a4: v62);
  if ( v58 != 0 )
  {
    v60 = 0;
    sub_14080D0E0(a1: &v59, a2: 0x1418E2C24LL);
    sub_140FFADB0(a1, a2: &v60, a3: 0, a4: 0);
    v55 = 0x80100004E554C4CLL;
    sub_1407D0F70(
      a1: (unsigned int)&v55,
      a2: (unsigned int)&v57,
      a3: (unsigned int)&v58,
      a4: (unsigned int)&v60,
      a5: (__int64)&v59,
      a6: 0,
      a7: 0,
      0);
    v12 = v57;
    if ( v57 != nullptr )
    {
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v57 + 40LL))(
        a1: v57,
        a2: &v59,
        a3: 4);
      if ( *((_DWORD *)v12 + 4) != 0 )
        goto LABEL_87;
      v13 = v57;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v57 + 40LL))(
        a1: v57,
        a2: a1 + 92,
        a3: 1);
      if ( *((_DWORD *)v13 + 4) != 0 )
        goto LABEL_87;
      if ( dword_141B5EB20 <= *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                        + 4LL) )
      {
LABEL_12:
        v14 = sub_1407E58C0(a1: &unk_141B5EAD0, a2: 80);
        *(_QWORD *)(v14 + 8) = -1;
        *(_DWORD *)(v14 + 16) = 0;
        *(_QWORD *)v14 = 0x141884988LL;
        *(_QWORD *)(v14 + 64) = 0xFF00000000LL;
        *(_QWORD *)(v14 + 24) = 0;
        *(_QWORD *)(v14 + 32) = 0;
        *(_QWORD *)(v14 + 40) = 0;
        *(_QWORD *)(v14 + 48) = 0;
        *(_QWORD *)(v14 + 56) = 0;
        v61 = v14;
        *(_BYTE *)(v14 + 72) = -1;
        if ( v59 != 0 )
        {
          v15 = 0;
          while ( 1 )
          {
            v17 = v57;
            (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v57 + 40LL))(
              a1: v57,
              a2: &v56,
              a3: 1);
            if ( *((_DWORD *)v17 + 4) != 0 )
              goto LABEL_86;
            if ( dword_141B5EB20 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(a1: &dword_141B5EB20);
              if ( dword_141B5EB20 == -1 )
              {
                sub_1407E53D0(
                  a1: (unsigned int)&unk_141B5EAD0,
                  a2: 1100142817,
                  a3: 0x2000,
                  a4: 80,
                  a5: 0,
                  a6: 1,
                  a7: 512,
                  a8: 4096);
                sub_141751048(a1: sub_140FB4840);
                sub_141750EA0(a1: &dword_141B5EB20);
              }
            }
            v18 = sub_1407E58C0(a1: &unk_141B5EAD0, a2: 80);
            *(_QWORD *)(v18 + 8) = -1;
            *(_DWORD *)(v18 + 16) = 0;
            *(_QWORD *)v18 = 0x141884988LL;
            *(_QWORD *)(v18 + 64) = 0xFF00000000LL;
            *(_QWORD *)(v18 + 24) = 0;
            *(_QWORD *)(v18 + 32) = 0;
            *(_QWORD *)(v18 + 40) = 0;
            *(_QWORD *)(v18 + 48) = 0;
            *(_QWORD *)(v18 + 56) = 0;
            *(_BYTE *)(v18 + 72) = -1;
            v20 = *(_DWORD *)(a1 + 84);
            v55 = (__int64)v57;
            if ( v57 != nullptr )
              _InterlockedIncrement(v57 + 2);
            LOBYTE(v53) = 1;
            LOBYTE(v19) = 1;
            v21 = sub_14119C960(a1: v18, a2: &v55, a3: v19, a4: &qword_141B5FDA8, a5: v20, a6: v15, a7: v53, a8: 0);
            v22 = (void (__fastcall ***)(_QWORD, __int64))v55;
            if ( v55 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v55 + 8)) == 0 )
              (**v22)(a1: v22, a2: 1);
            if ( v21 == 0 )
            {
              sub_140FAC350(a1: v18);
              sub_140FAC350(a1: v61);
              v49 = 0;
              goto LABEL_88;
            }
            v23 = qword_141B5FDB8;
            if ( *(_BYTE *)(qword_141B5FDB8 + 89) != 0 )
              break;
LABEL_40:
            v32 = qword_141B5FDC0;
            if ( *(_BYTE *)(qword_141B5FDC0 + 89) == 0 )
              goto LABEL_62;
            if ( **(_QWORD **)(qword_141B5FDC0 + 128) == *(_QWORD *)(*(_QWORD *)(qword_141B5FDC0 + 128) + 8LL) )
            {
LABEL_60:
              v34 = 0;
              goto LABEL_61;
            }
            v33 = *(_QWORD *)(v18 + 32);
            v34 = 0;
            if ( (int)v33 >= 0 )
            {
              if ( *(_QWORD *)(qword_141B5FDC0 + 40) == 0
                && (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)qword_141B5FDC0 + 48LL))(
                     a1: qword_141B5FDC0,
                     a2: 0) > (unsigned __int64)(unsigned int)v33 )
              {
                goto LABEL_59;
              }
              v35 = *(__int64 **)(v32 + 32);
              v36 = (__int64 *)v35[1];
              v37 = v35;
              if ( *((_BYTE *)v36 + 25) == 0 )
              {
                v37 = *(__int64 **)(v32 + 32);
                do
                {
                  v38 = v36 + 2;
                  if ( *((_DWORD *)v36 + 7) >= (int)v33 )
                  {
                    v37 = v36;
                    v38 = v36;
                  }
                  v36 = (__int64 *)*v38;
                }
                while ( *(_BYTE *)(*v38 + 25) == 0 );
              }
              if ( *((_BYTE *)v37 + 25) != 0 )
              {
                v34 = 0;
              }
              else
              {
                if ( *((_DWORD *)v37 + 7) > (int)v33 )
                  goto LABEL_60;
                v34 = 0;
                if ( v37 != v35 )
                {
                  LODWORD(v33) = *((_DWORD *)v37 + 8);
                  if ( (int)v33 < 0 )
                    goto LABEL_60;
LABEL_59:
                  v34 = *(_QWORD *)(**(_QWORD **)(v32 + 128) + 8LL * (unsigned int)v33);
                }
              }
            }
LABEL_61:
            *(_QWORD *)(v18 + 32) = v34;
LABEL_62:
            v39 = qword_141B5FE28;
            if ( *(_BYTE *)(qword_141B5FE28 + 89) != 0 )
            {
              if ( **(_QWORD **)(qword_141B5FE28 + 128) != *(_QWORD *)(*(_QWORD *)(qword_141B5FE28 + 128) + 8LL) )
              {
                v40 = *(_QWORD *)(v18 + 48);
                v41 = 0;
                if ( (int)v40 < 0 )
                {
LABEL_79:
                  *(_QWORD *)(v18 + 48) = v41;
                  goto LABEL_80;
                }
                if ( *(_QWORD *)(qword_141B5FE28 + 40) == 0
                  && (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)qword_141B5FE28 + 48LL))(
                       a1: qword_141B5FE28,
                       a2: 0) > (unsigned __int64)(unsigned int)v40 )
                {
                  goto LABEL_77;
                }
                v42 = *(__int64 **)(v39 + 32);
                v43 = (__int64 *)v42[1];
                v44 = v42;
                if ( *((_BYTE *)v43 + 25) == 0 )
                {
                  v44 = *(__int64 **)(v39 + 32);
                  do
                  {
                    v45 = v43 + 2;
                    if ( *((_DWORD *)v43 + 7) >= (int)v40 )
                    {
                      v44 = v43;
                      v45 = v43;
                    }
                    v43 = (__int64 *)*v45;
                  }
                  while ( *(_BYTE *)(*v45 + 25) == 0 );
                }
                if ( *((_BYTE *)v44 + 25) != 0 )
                {
                  v41 = 0;
                  goto LABEL_79;
                }
                if ( *((_DWORD *)v44 + 7) <= (int)v40 )
                {
                  v41 = 0;
                  if ( v44 == v42 )
                    goto LABEL_79;
                  LODWORD(v40) = *((_DWORD *)v44 + 8);
                  if ( (int)v40 >= 0 )
                  {
LABEL_77:
                    v41 = *(_QWORD *)(**(_QWORD **)(v39 + 128) + 8LL * (unsigned int)v40);
                    goto LABEL_79;
                  }
                }
              }
              v41 = 0;
              goto LABEL_79;
            }
LABEL_80:
            v54 = 0;
            v55 = v18;
            v46 = *(_QWORD *)(a2 + 56);
            if ( v46 == 0 )
              goto LABEL_101;
            (*(void (__fastcall **)(__int64, __int64 *, char *))(*(_QWORD *)v46 + 16LL))(a1: v46, a2: &v55, a3: &v54);
            if ( v54 != 0 )
            {
              v47 = sub_141758910(a1: v18, a2: 0, a3: &unk_141A7F570, a4: &unk_141AAF310, a5: 0);
              if ( v47 != 0 )
              {
                LOBYTE(v48) = 1;
                sub_140F6C770(a1, a2: v47, a3: v48);
              }
            }
            else
            {
              sub_140FAC350(a1: v18);
            }
            if ( ++v15 >= v59 )
              goto LABEL_86;
          }
          v24 = v15;
          v25 = (__int64 *)(v18 + 24);
          if ( **(_QWORD **)(qword_141B5FDB8 + 128) != *(_QWORD *)(*(_QWORD *)(qword_141B5FDB8 + 128) + 8LL) )
          {
            v26 = *v25;
            v27 = 0;
            if ( (int)*v25 < 0 )
            {
LABEL_39:
              *v25 = v27;
              v15 = v24;
              goto LABEL_40;
            }
            if ( *(_QWORD *)(qword_141B5FDB8 + 40) == 0
              && (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)qword_141B5FDB8 + 48LL))(
                   a1: qword_141B5FDB8,
                   a2: 0) > (unsigned __int64)(unsigned int)v26 )
            {
              goto LABEL_55;
            }
            v28 = *(__int64 **)(v23 + 32);
            v29 = (__int64 *)v28[1];
            v30 = v28;
            if ( *((_BYTE *)v29 + 25) == 0 )
            {
              v30 = *(__int64 **)(v23 + 32);
              do
              {
                v31 = v29 + 2;
                if ( *((_DWORD *)v29 + 7) >= (int)v26 )
                {
                  v30 = v29;
                  v31 = v29;
                }
                v29 = (__int64 *)*v31;
              }
              while ( *(_BYTE *)(*v31 + 25) == 0 );
            }
            if ( *((_BYTE *)v30 + 25) == 0 && *((_DWORD *)v30 + 7) <= (int)v26 )
            {
              v27 = 0;
              if ( v30 == v28 )
                goto LABEL_39;
              LODWORD(v26) = *((_DWORD *)v30 + 8);
              if ( (int)v26 >= 0 )
              {
LABEL_55:
                v27 = *(_QWORD *)(**(_QWORD **)(v23 + 128) + 8LL * (unsigned int)v26);
                goto LABEL_39;
              }
            }
          }
          v27 = 0;
          goto LABEL_39;
        }
LABEL_86:
        sub_140FAC350(a1: v61);
LABEL_87:
        v49 = 1;
LABEL_88:
        v50 = v57;
        if ( v57 != nullptr && _InterlockedDecrement(v57 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v50)(a1: v50, a2: 1);
        v51 = v60;
        if ( v60 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v60 - 4)) == 0 )
          sub_1412EC9A0(a1: v51 - 4);
        if ( v49 == 0 )
          goto LABEL_96;
        goto LABEL_95;
      }
LABEL_102:
      sub_141750E08(a1: &dword_141B5EB20);
      if ( dword_141B5EB20 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5EAD0,
          a2: 1100142817,
          a3: 0x2000,
          a4: 80,
          a5: 0,
          a6: 1,
          a7: 512,
          a8: 4096);
        sub_141751048(a1: sub_140FB4840);
        sub_141750EA0(a1: &dword_141B5EB20);
      }
      goto LABEL_12;
    }
    v16 = v60;
    if ( v60 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v60 - 4)) == 0 )
      sub_1412EC9A0(a1: v16 - 4);
  }
LABEL_95:
  LOWORD(qword_141B60330) = 3569;
LABEL_96:
  v52 = (void (__fastcall ***)(_QWORD, __int64))v58;
  if ( v58 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58 + 8)) == 0 )
    (**v52)(a1: v52, a2: 1);
}
