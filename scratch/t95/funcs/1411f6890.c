_QWORD *__fastcall sub_1411F6890(__int64 a1, unsigned int a2, _DWORD *a3, __int64 a4, char a5, unsigned int a6)
{
  int v9; // esi
  __int64 v10; // rdi
  _QWORD *result; // rax
  __int64 v12; // rbx
  __int64 *v13; // rax
  __int64 v14; // rax
  __int64 v15; // rbx
  __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 *v18; // rdx
  unsigned int v19; // ebx
  __int64 *v20; // rcx
  __int64 v21; // rcx
  _DWORD *v22; // r13
  int v23; // esi
  __int64 v24; // rax
  unsigned __int8 v25; // di
  unsigned __int8 v26; // r12
  char v27; // di
  _QWORD *v28; // rsi
  unsigned __int8 v29; // bl
  __int64 v30; // rax
  char v31; // r13
  int v32; // esi
  __int64 v33; // rcx
  __int64 v34; // rax
  __int64 v35; // rdi
  __int64 v36; // rcx
  __int64 v37; // rcx
  __int64 v38; // rcx
  __int64 v39; // rax
  __int64 v40; // rdi
  __int64 v41; // rcx
  __int64 v42; // rcx
  __int64 v43; // rcx
  __int64 v44; // rax
  __int64 v45; // rdi
  __int64 v46; // rcx
  __int64 v47; // rcx
  __int64 v48; // rcx
  __int64 v49; // rax
  __int64 v50; // rdi
  __int64 v51; // rcx
  __int64 v52; // rcx
  int v53; // r12d
  __int64 v54; // rcx
  __int64 v55; // rax
  __int64 v56; // rdi
  __int64 v57; // rcx
  __int64 v58; // rcx
  __int64 v59; // rcx
  __int64 v60; // rax
  __int64 v61; // rdi
  __int64 v62; // rcx
  __int64 v63; // rcx
  __int64 v64; // rcx
  __int64 v65; // rax
  __int64 v66; // rdi
  __int64 v67; // rcx
  __int64 v68; // rcx
  __int64 v69; // rcx
  __int64 v70; // rax
  __int64 v71; // rdi
  __int64 v72; // rcx
  __int64 v73; // rcx
  __int64 v74; // rcx
  __int64 v75; // rax
  __int64 v76; // rsi
  __int64 v77; // rcx
  __int64 v78; // rcx
  __int64 v79; // rcx
  __int64 v80; // rax
  __int64 v81; // rsi
  __int64 v82; // rcx
  __int64 v83; // rcx
  __int64 v84; // rcx
  __int64 v85; // rax
  __int64 v86; // rsi
  __int64 v87; // rcx
  __int64 v88; // rcx
  __int64 v89; // rcx
  __int64 v90; // rax
  __int64 v91; // rcx
  __int64 v92; // rsi
  __int64 v93; // rcx
  __int64 v94; // rcx
  __int64 v95; // rcx
  __int64 v96; // rax
  __int64 v97; // rax
  _QWORD v98[3]; // [rsp+28h] [rbp-58h] BYREF
  int v99; // [rsp+44h] [rbp-3Ch]
  int v100; // [rsp+48h] [rbp-38h]
  int v101; // [rsp+4Ch] [rbp-34h]
  __int64 v102; // [rsp+50h] [rbp-30h] BYREF
  char v103; // [rsp+5Fh] [rbp-21h]
  __int64 v104; // [rsp+60h] [rbp-20h] BYREF
  __int64 v105; // [rsp+68h] [rbp-18h]
  unsigned __int8 v106; // [rsp+77h] [rbp-9h]
  _QWORD v107[9]; // [rsp+78h] [rbp-8h] BYREF

  v107[1] = -2;
  v106 = sub_1411D9B80(a1, a4);
  v9 = 1049072;
  v10 = a1;
LABEL_2:
  result = *(_QWORD **)(v10 + 176);
  v12 = result[9];
  if ( v12 != 0 )
  {
    result = (_QWORD *)sub_14155C8C0(result[9], a1, a2, v106);
    if ( result == (_QWORD *)a3 )
      return result;
    v22 = result;
    sub_14155C8C0(v12, a1, a2, v106);
    if ( a3 != nullptr )
    {
      v23 = a3[3];
      v101 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a3 + 528LL))(a3);
      v24 = (*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a3 + 1024LL))(a3, a1, 0);
      v100 = v23;
      if ( v24 != 0 )
      {
LABEL_27:
        v25 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v24 + 80LL))(v24);
        goto LABEL_31;
      }
      if ( *(_BYTE *)(a1 + 186) != 0 || (v96 = sub_140E68C40(a1)) == 0 )
      {
        v25 = 0;
      }
      else
      {
        v25 = 0;
        v24 = (*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a3 + 1024LL))(a3, v96, 0);
        if ( v24 != 0 )
          goto LABEL_27;
      }
    }
    else
    {
      v25 = 0;
      v100 = -1;
      v101 = 0;
    }
LABEL_31:
    v26 = v25;
    v103 = -1;
    if ( v22 == nullptr )
    {
      v99 = -1;
      v29 = 0;
      v31 = 0;
      goto LABEL_39;
    }
    v99 = v22[3];
    v27 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v22 + 528LL))(v22);
    v28 = (_QWORD *)(*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)v22 + 1024LL))(v22, a1, 0);
    if ( v28 != nullptr )
      goto LABEL_33;
    if ( *(_BYTE *)(a1 + 186) != 0 || (v97 = sub_140E68C40(a1)) == 0 )
    {
      v29 = 0;
    }
    else
    {
      v29 = 0;
      v28 = (_QWORD *)(*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)v22 + 1024LL))(v22, v97, 0);
      if ( v28 != nullptr )
      {
LABEL_33:
        v29 = (*(__int64 (__fastcall **)(_QWORD *))(*v28 + 80LL))(v28);
        v30 = v28[2];
        if ( v30 != 0 )
          v103 = *(_BYTE *)(v30 + 40);
      }
    }
    v31 = v27;
LABEL_39:
    sub_1407C9510(v98);
    v32 = *(_DWORD *)(a1 + 12);
    v34 = sub_14083D4F0(v33);
    LODWORD(v105) = v32;
    v104 = v34 + 40;
    v107[0] = 0;
    v35 = sub_1412EC810(264, 7);
    *(_QWORD *)v35 = 0x700000000LL;
    strcpy((char *)(v35 + 8), "team_id");
    if ( v107[0] != 0 )
    {
      v36 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v36);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v35);
    v107[0] = v35 + 4;
    sub_14013B810(v98, v107, &v104);
    v37 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v37 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v39 = sub_14083D4F0(v38);
    LODWORD(v105) = (unsigned __int8)a2;
    v104 = v39 + 56;
    v107[0] = 0;
    v40 = sub_1412EC810(264, 17);
    *(_QWORD *)v40 = 0x1100000000LL;
    strcpy((char *)(v40 + 8), "responsibility_id");
    if ( v107[0] != 0 )
    {
      v41 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v41);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v40);
    v107[0] = v40 + 4;
    sub_14013B810(v98, v107, &v104);
    v42 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v42 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v44 = sub_14083D4F0(v43);
    LODWORD(v105) = v29;
    v104 = v44 + 56;
    v107[0] = 0;
    v45 = sub_1412EC810(264, 16);
    *(_QWORD *)v45 = 0x1000000000LL;
    strcpy((char *)(v45 + 8), "old_staff_job_id");
    if ( v107[0] != 0 )
    {
      v46 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v46);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v45);
    v107[0] = v45 + 4;
    sub_14013B810(v98, v107, &v104);
    v47 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v47 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v49 = sub_14083D4F0(v48);
    LODWORD(v105) = v26;
    v104 = v49 + 56;
    v107[0] = 0;
    v50 = sub_1412EC810(264, 16);
    *(_QWORD *)v50 = 0x1000000000LL;
    strcpy((char *)(v50 + 8), "new_staff_job_id");
    if ( v107[0] != 0 )
    {
      v51 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v51);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v50);
    v107[0] = v50 + 4;
    sub_14013B810(v98, v107, &v104);
    v52 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v52 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v53 = v99;
    v55 = sub_14083D4F0(v54);
    LODWORD(v105) = v53;
    v104 = v55 + 40;
    v107[0] = 0;
    v56 = sub_1412EC810(264, 12);
    *(_QWORD *)v56 = 0xC00000000LL;
    strcpy((char *)(v56 + 8), "old_staff_id");
    if ( v107[0] != 0 )
    {
      v57 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v57);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v56);
    v107[0] = v56 + 4;
    sub_14013B810(v98, v107, &v104);
    v58 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v58 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v60 = sub_14083D4F0(v59);
    LODWORD(v105) = v100;
    v104 = v60 + 40;
    v107[0] = 0;
    v61 = sub_1412EC810(264, 12);
    *(_QWORD *)v61 = 0xC00000000LL;
    strcpy((char *)(v61 + 8), "new_staff_id");
    if ( v107[0] != 0 )
    {
      v62 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v62);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v61);
    v107[0] = v61 + 4;
    sub_14013B810(v98, v107, &v104);
    v63 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v63 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v65 = sub_14083D4F0(v64);
    LODWORD(v105) = v103;
    v104 = v65 + 40;
    v107[0] = 0;
    v66 = sub_1412EC810(264, 14);
    *(_QWORD *)v66 = 0xE00000000LL;
    strcpy((char *)(v66 + 8), "old_staff_team");
    if ( v107[0] != 0 )
    {
      v67 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v67);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v66);
    v107[0] = v66 + 4;
    sub_14013B810(v98, v107, &v104);
    v68 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v68 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v70 = sub_14083D4F0(v69);
    LODWORD(v105) = (char)v106;
    v104 = v70 + 40;
    v107[0] = 0;
    v71 = sub_1412EC810(264, 14);
    *(_QWORD *)v71 = 0xE00000000LL;
    strcpy((char *)(v71 + 8), "new_staff_team");
    if ( v107[0] != 0 )
    {
      v72 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v72);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v71);
    v107[0] = v71 + 4;
    sub_14013B810(v98, v107, &v104);
    v73 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v73 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v75 = sub_14083D4F0(v74);
    LOBYTE(v105) = v31;
    v104 = v75 + 24;
    v107[0] = 0;
    v76 = sub_1412EC810(264, 9);
    *(_QWORD *)v76 = 0x900000000LL;
    strcpy((char *)(v76 + 8), "was_human");
    if ( v107[0] != 0 )
    {
      v77 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v77);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v76);
    v107[0] = v76 + 4;
    sub_14013B810(v98, v107, &v104);
    v78 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v78 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v80 = sub_14083D4F0(v79);
    LOBYTE(v105) = v101;
    v104 = v80 + 24;
    v107[0] = 0;
    v81 = sub_1412EC810(264, 8);
    *(_QWORD *)v81 = 0x800000000LL;
    strcpy((char *)(v81 + 8), "is_human");
    if ( v107[0] != 0 )
    {
      v82 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v82);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v81);
    v107[0] = v81 + 4;
    sub_14013B810(v98, v107, &v104);
    v83 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v83 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v85 = sub_14083D4F0(v84);
    LOBYTE(v105) = a5;
    v104 = v85 + 24;
    v107[0] = 0;
    v86 = sub_1412EC810(264, 14);
    *(_QWORD *)v86 = 0xE00000000LL;
    strcpy((char *)(v86 + 8), "auto_delegated");
    if ( v107[0] != 0 )
    {
      v87 = v107[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
        sub_1412EC9A0(v87);
    }
    v107[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v86);
    v107[0] = v86 + 4;
    sub_14013B810(v98, v107, &v104);
    v88 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v88 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v107[0] = 0;
    sub_14082DAF0(a6, v107);
    v90 = sub_14083D4F0(v89);
    v105 = 0;
    v91 = v107[0];
    if ( v107[0] != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v107[0] - 4LL));
    v105 = v91;
    v104 = v90 + 136;
    v102 = 0;
    v92 = sub_1412EC810(264, 15);
    *(_QWORD *)v92 = 0xF00000000LL;
    strcpy((char *)(v92 + 8), "change_location");
    if ( v102 != 0 )
    {
      v93 = v102 - 4;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v102 - 4)) == 0 )
        sub_1412EC9A0(v93);
    }
    v102 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v92);
    v102 = v92 + 4;
    sub_14013B810(v98, &v102, &v104);
    v94 = v102;
    if ( v102 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v102 - 4)) == 0 )
      sub_1412EC9A0(v94 - 4);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v104 + 16LL))(v104, &v104);
    v95 = v107[0];
    if ( v107[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107[0] - 4LL)) == 0 )
      sub_1412EC9A0(v95 - 4);
    sub_14013B9C0(qword_141ABE000, &unk_141B63A08, v98);
    return (_QWORD *)sub_14083B0A0(v98);
  }
  if ( *(_BYTE *)(v10 + 186) == 0 )
  {
    v13 = *(__int64 **)(v10 + 24);
    if ( v13 == *(__int64 **)(v10 + 32)
      || (v14 = *v13) == 0
      || (v15 = *(_QWORD *)(v14 + 128)) == 0
      || (v16 = v15 + *(int *)(*(_QWORD *)(v15 + 8) + 4LL) + 8,
          (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v16 + 528LL))(v16) == 0)
      || (v17 = v15 + *(int *)(*(_QWORD *)(v15 + 8) + 4LL) + 8,
          (result = (_QWORD *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v17 + 1752LL))(v17)) == nullptr) )
    {
      for ( result = *(_QWORD **)(v10 + 280); result != *(_QWORD **)(v10 + 288); ++result )
      {
        v18 = (__int64 *)*result;
        if ( *(_QWORD *)(*result + 8LL) == v10 )
        {
          v19 = *((unsigned __int8 *)v18 + 48);
          if ( v19 <= 0x14 )
          {
            if ( _bittest(&v9, v19) )
            {
              v10 = *v18;
              if ( *v18 != 0 )
              {
                result = *(_QWORD **)(v10 + 24);
                if ( result != *(_QWORD **)(v10 + 32) )
                {
                  v20 = (__int64 *)*result;
                  if ( *result != 0 )
                  {
                    if ( *((_BYTE *)v20 + 40) != 0 )
                    {
                      result = (_QWORD *)sub_1411A41D0();
                      if ( result == nullptr )
                        return result;
                    }
                    else
                    {
                      result = (_QWORD *)v20[16];
                      if ( result == nullptr )
                        return result;
                    }
                    v21 = (__int64)result + *(int *)(result[1] + 4LL) + 8;
                    result = (_QWORD *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v21 + 1760LL))(v21);
                    if ( result != nullptr )
                      goto LABEL_2;
                  }
                }
              }
              return result;
            }
          }
        }
      }
    }
  }
  return result;
}
