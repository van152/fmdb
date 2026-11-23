char __fastcall sub_14101D990(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rcx
  char result; // al
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rcx
  __int64 v9; // rax
  int v10; // ecx
  __int64 v11; // rcx
  __int64 v12; // rcx

  if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*a2 + 224LL))(a2) == 0 )
    return 0;
  v4 = (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2);
  result = 0;
  switch ( v4 )
  {
    case 0LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 0 )
        return 0;
      if ( a2[14] == 0 )
        return 0;
      v6 = a2[11];
      if ( v6 != 0 )
      {
        v7 = *(_QWORD *)(v6 + 176);
        if ( v7 == 0 || !sub_1409083C0(v7) )
          return 0;
      }
      goto LABEL_34;
    case 1LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 1
        || (*(unsigned __int8 (__fastcall **)(_QWORD *))(*a2 + 1312LL))(a2) != 0 )
      {
        return 0;
      }
      v8 = (*(__int64 (__fastcall **)(_QWORD *))(*a2 + 1712LL))(a2);
      result = 0;
      if ( v8 == 0 || (_QWORD *)(a1 + 1104) == a2 )
        return result;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*a2 + 1352LL))(a2) == 0 )
        goto LABEL_34;
      return 0;
    case 3LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 3
        || (*(unsigned __int8 (__fastcall **)(_QWORD *))(*a2 + 352LL))(a2) != 0
        || a2[27] == 0 )
      {
        return 0;
      }
      goto LABEL_34;
    case 5LL:
      goto LABEL_34;
    case 9LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 9 )
        return 0;
      v9 = a2[46];
      if ( *(_QWORD *)(v9 + 240) == 0 || *(_DWORD *)(v9 + 12) == 215446 )
        return 0;
      goto LABEL_34;
    case 24LL:
      v10 = (*(__int64 (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2);
      result = 0;
      if ( v10 != 24 || (_BYTE)word_141B60320 == 0 )
        return result;
      v11 = a2[6];
      if ( v11 == 0 || (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v11 + 352LL))(v11) != 0 )
        return 0;
LABEL_34:
      result = 1;
      break;
    case 25LL:
      if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 25 )
        return 0;
      v12 = a2[22];
      if ( v12 == 0 || !sub_1409083C0(v12) || (unsigned __int8)sub_140EBF780(a2) != 0 )
        return 0;
      goto LABEL_34;
    default:
      return result;
  }
  return result;
}
