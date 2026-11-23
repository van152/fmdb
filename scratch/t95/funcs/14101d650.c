char __fastcall sub_14101D650(__int64 a1, _QWORD *a2)
{
  __int64 v4; // r14
  _BYTE *v5; // rax
  __int64 v6; // rcx
  _BYTE *v7; // rdi
  __int64 v8; // rax
  __int64 v9; // r15
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rax
  __int64 v13; // r12
  __int64 v14; // rdi
  __int64 v15; // r9
  char v16; // di
  __int64 v17; // rcx
  char result; // al
  __int64 v19; // rax
  __int64 v20; // rdx
  _QWORD *v21; // rax
  _BYTE *v22; // rax
  _BYTE *v23; // rdi
  __int64 v24; // rax
  int v25; // ecx
  __int64 v26; // rax
  __int64 *v27; // rcx
  __int64 v28; // rcx
  __int64 v29; // rax
  __int64 v30; // rcx
  __int64 v31; // [rsp+28h] [rbp-18h] BYREF
  char v32; // [rsp+30h] [rbp-10h]
  __int64 v33; // [rsp+38h] [rbp-8h]

  v33 = -2;
  if ( (unsigned __int8)sub_14101D990(a1, a2) == 0 )
    return 0;
  v4 = a1 + 1104;
  v5 = (_BYTE *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + 1104) + 1032LL))(a1 + 1104);
  if ( v5 != nullptr
    && ((v7 = v5, v5[28] > 1u) || (*(unsigned __int8 (__fastcall **)(_BYTE *))(*(_QWORD *)v5 + 104LL))(v5) >= 2u)
    && (v8 = *((_QWORD *)v7 + 2)) != 0
    && *(_BYTE *)(v8 + 47) == 0 )
  {
    v9 = *(_QWORD *)(v8 + 48);
  }
  else
  {
    v9 = 0;
  }
  v10 = *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 176);
  if ( v10 != 0 && (v11 = *(_QWORD *)(v10 + 16)) != 0 && (v12 = *(_QWORD *)(v11 + 16)) != 0 )
    v13 = *(_QWORD *)(v12 + 48);
  else
    v13 = 0;
  v14 = qword_141ABDFE8;
  v32 = 0;
  v31 = sub_14083D4F0(v6) + 24;
  LOBYTE(v15) = 1;
  v16 = sub_140800A10(v14, &unk_141ABE810, &v31, v15);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, &v31);
  v17 = (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2);
  result = 0;
  switch ( v17 )
  {
    case 0LL:
    case 5LL:
    case 25LL:
      goto LABEL_15;
    case 1LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 1
        || (*(__int64 (__fastcall **)(_QWORD *))(*a2 + 1760LL))(a2) != 0
        && (v16 != 0 || *(_BYTE *)((*(__int64 (__fastcall **)(_QWORD *))(*a2 + 1760LL))(a2) + 1067) == 0) )
      {
        return 0;
      }
      goto LABEL_15;
    case 3LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 3 )
        return 0;
      if ( v16 != 0 )
      {
        v19 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v4 + 656LL))(v4);
        if ( v19 == 0 || *(_BYTE *)(v19 + 47) != 0 || (v21 = *(_QWORD **)(v19 + 48)) == nullptr )
        {
          v22 = (_BYTE *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v4 + 1032LL))(v4);
          if ( v22 != nullptr
            && ((v23 = v22, v22[28] > 1u)
             || (*(unsigned __int8 (__fastcall **)(_BYTE *))(*(_QWORD *)v22 + 104LL))(v22) >= 2u)
            && (v24 = *((_QWORD *)v23 + 2)) != 0
            && *(_BYTE *)(v24 + 47) == 0 )
          {
            v21 = *(_QWORD **)(v24 + 48);
          }
          else
          {
            v21 = nullptr;
          }
        }
        if ( v21 != a2 )
        {
          LOBYTE(v20) = 1;
          if ( (unsigned __int8)sub_1411D97B0(a2, v20) != 0 )
            return 0;
        }
      }
      goto LABEL_15;
    case 24LL:
      v25 = (*(__int64 (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2);
      result = 0;
      if ( v25 != 24 || (_BYTE)word_141B60320 == 0 )
        return result;
      v26 = a2[6];
      if ( v26 != v13 && v26 != v9 && v16 == 1 )
      {
        v27 = *(__int64 **)(v26 + 24);
        if ( v27 != *(__int64 **)(v26 + 32) )
        {
          v28 = *v27;
          if ( v28 != 0 )
          {
            v29 = *(_BYTE *)(v28 + 40) != 0 ? sub_1411A41D0(v28) : *(_QWORD *)(v28 + 128);
            if ( v29 != 0 )
            {
              v30 = v29 + *(int *)(*(_QWORD *)(v29 + 8) + 4LL) + 8;
              if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v30 + 1760LL))(v30) != 0 )
                return 0;
            }
          }
        }
      }
LABEL_15:
      result = 1;
      break;
    default:
      return result;
  }
  return result;
}
